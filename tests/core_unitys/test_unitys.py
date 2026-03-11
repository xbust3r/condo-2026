"""Unit tests for Unitys domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestUnitys(unittest.TestCase):
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
        
        self.assertEqual(unity.id, 1)
        self.assertEqual(unity.name, "Apartamento 101")
        self.assertEqual(unity.code, "APT101")
        self.assertEqual(unity.description, "Apartamento de 2 habitaciones")
        self.assertEqual(unity.size, 85.50)
        self.assertEqual(unity.percentage, 2.5)
        self.assertEqual(unity.type, "residencial")
        self.assertEqual(unity.floor, 1)
        self.assertEqual(unity.unit, "101")
        self.assertEqual(unity.building_id, 1)
        self.assertEqual(unity.unity_type_id, 1)

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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Penthouse 501")
        self.assertEqual(result["code"], "PH501")
        self.assertEqual(result["description"], "Penthouse de lujo")
        self.assertEqual(result["size"], 150.75)
        self.assertEqual(result["percentage"], 5.0)
        self.assertEqual(result["type"], "residencial")
        self.assertEqual(result["floor"], 5)
        self.assertEqual(result["unit"], "501")
        self.assertEqual(result["building_id"], 2)
        self.assertEqual(result["unity_type_id"], 3)
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_unitys_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
        from chalicelib.dddpy.core_unitys.infrastructure.unitys import DBUnitys
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBUnitys)
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
        
        self.assertIsInstance(unity, Unitys)
        self.assertEqual(unity.id, 1)
        self.assertEqual(unity.name, "Local 101")
        self.assertEqual(unity.code, "LC101")
        self.assertEqual(unity.size, 45.00)

    def test_unitys_optional_fields(self):
        """Test Unitys with optional fields as None."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
        
        unity = Unitys(
            id=1,
            name="Minimal Unity",
            code="MIN001"
        )
        
        self.assertIsNone(unity.description)
        self.assertIsNone(unity.size)
        self.assertIsNone(unity.percentage)
        self.assertIsNone(unity.type)
        self.assertIsNone(unity.floor)
        self.assertIsNone(unity.unit)
        self.assertIsNone(unity.building_id)
        self.assertIsNone(unity.unity_type_id)
        self.assertIsNone(unity.created_at)
        self.assertIsNone(unity.updated_at)


class TestUnitysExceptions(unittest.TestCase):
    """Test cases for Unitys exceptions."""

    def test_unitys_not_found_exception(self):
        """Test UnitysNotFoundException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnitysNotFoundException
        
        exc = UnitysNotFoundException()
        self.assertEqual(exc.message, "Unitys not found")
        self.assertEqual(exc.status_code, 404)

    def test_unitys_already_exists_exception(self):
        """Test UnitysAlreadyExistsException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnitysAlreadyExistsException
        
        exc = UnitysAlreadyExistsException()
        self.assertEqual(exc.message, "Unitys already exists")
        self.assertEqual(exc.status_code, 409)

    def test_unitys_validation_exception(self):
        """Test UnitysValidationException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnitysValidationException
        
        exc = UnitysValidationException()
        self.assertEqual(exc.message, "Unitys validation failed")
        self.assertEqual(exc.status_code, 400)


class TestUnitysSuccessMessages(unittest.TestCase):
    """Test cases for Unitys success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_unitys.domain.unitys_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.UNITYS_CREATED, "Unitys created successfully")
        self.assertEqual(SuccessMessages.UNITYS_UPDATED, "Unitys updated successfully")
        self.assertEqual(SuccessMessages.UNITYS_DELETED, "Unitys deleted successfully")
        self.assertEqual(SuccessMessages.UNITYS_RETRIEVED, "Unitys retrieved successfully")
        self.assertEqual(SuccessMessages.UNITYS_LISTED, "Unitys listed successfully")


if __name__ == "__main__":
    unittest.main()
