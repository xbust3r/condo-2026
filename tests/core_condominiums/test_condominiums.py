"""Unit tests for Condominiums domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestCondominiums(unittest.TestCase):
    """Test cases for Condominiums domain class."""

    def test_condominium_creation(self):
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
        
        self.assertEqual(condo.id, 1)
        self.assertEqual(condo.name, "Test Condo")
        self.assertEqual(condo.code, "TC001")
        self.assertEqual(condo.description, "A test condominium")
        self.assertEqual(condo.size, 1000.50)
        self.assertEqual(condo.percentage, 5.5)

    def test_condominium_to_dict(self):
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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Test Condo")
        self.assertEqual(result["code"], "TC001")
        self.assertEqual(result["description"], "A test condominium")
        self.assertEqual(result["size"], 1000.50)
        self.assertEqual(result["percentage"], 5.5)
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_condominium_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
        from chalicelib.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBCondominiums)
        mock_db.id = 1
        mock_db.name = "Test Condo"
        mock_db.code = "TC001"
        mock_db.description = "A test condominium"
        mock_db.size = 1000.50
        mock_db.percentage = 5.5
        mock_db.created_at = now
        mock_db.updated_at = now
        
        condo = Condominiums.from_db(mock_db)
        
        self.assertIsInstance(condo, Condominiums)
        self.assertEqual(condo.id, 1)
        self.assertEqual(condo.name, "Test Condo")
        self.assertEqual(condo.code, "TC001")

    def test_condominium_optional_fields(self):
        """Test Condominium with optional fields as None."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
        
        condo = Condominiums(
            id=1,
            name="Minimal Condo",
            code="MC001"
        )
        
        self.assertIsNone(condo.description)
        self.assertIsNone(condo.size)
        self.assertIsNone(condo.percentage)
        self.assertIsNone(condo.created_at)
        self.assertIsNone(condo.updated_at)


class TestCondominiumExceptions(unittest.TestCase):
    """Test cases for Condominium exceptions."""

    def test_condominium_not_found_exception(self):
        """Test CondominiumNotFoundException."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import (
            CondominiumNotFoundException
        )
        
        exc = CondominiumNotFoundException()
        self.assertEqual(exc.message, "Condominium not found")
        self.assertEqual(exc.status_code, 404)

    def test_condominium_already_exists_exception(self):
        """Test CondominiumAlreadyExistsException."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import (
            CondominiumAlreadyExistsException
        )
        
        exc = CondominiumAlreadyExistsException()
        self.assertEqual(exc.message, "Condominium already exists")
        self.assertEqual(exc.status_code, 409)

    def test_condominium_validation_exception(self):
        """Test CondominiumValidationException."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import (
            CondominiumValidationException
        )
        
        exc = CondominiumValidationException()
        self.assertEqual(exc.message, "Condominium validation failed")
        self.assertEqual(exc.status_code, 400)


class TestCondominiumSuccessMessages(unittest.TestCase):
    """Test cases for Condominium success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_condominiums.domain.condominiums_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.CONDOMINIUM_CREATED, "Condominium created successfully")
        self.assertEqual(SuccessMessages.CONDOMINIUM_UPDATED, "Condominium updated successfully")
        self.assertEqual(SuccessMessages.CONDOMINIUM_DELETED, "Condominium deleted successfully")
        self.assertEqual(SuccessMessages.CONDOMINIUM_RETRIEVED, "Condominium retrieved successfully")
        self.assertEqual(SuccessMessages.CONDOMINIUMS_LISTED, "Condominiums listed successfully")


if __name__ == "__main__":
    unittest.main()
