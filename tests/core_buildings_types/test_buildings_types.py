"""Unit tests for BuildingsTypes domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestBuildingsTypes(unittest.TestCase):
    """Test cases for BuildingsTypes domain class."""

    def test_building_type_creation(self):
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
        
        self.assertEqual(building_type.id, 1)
        self.assertEqual(building_type.name, "Residential")
        self.assertEqual(building_type.code, "RES")
        self.assertEqual(building_type.description, "Residential building type")

    def test_building_type_to_dict(self):
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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Residential")
        self.assertEqual(result["code"], "RES")
        self.assertEqual(result["description"], "Residential building type")
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_building_type_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
        from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBBuildingsTypes)
        mock_db.id = 1
        mock_db.name = "Residential"
        mock_db.code = "RES"
        mock_db.description = "Residential building type"
        mock_db.created_at = now
        mock_db.updated_at = now
        
        building_type = BuildingsTypes.from_db(mock_db)
        
        self.assertIsInstance(building_type, BuildingsTypes)
        self.assertEqual(building_type.id, 1)
        self.assertEqual(building_type.name, "Residential")
        self.assertEqual(building_type.code, "RES")

    def test_building_type_optional_fields(self):
        """Test BuildingsTypes with optional fields as None."""
        from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
        
        building_type = BuildingsTypes(
            id=1,
            name="Commercial",
            code="COM"
        )
        
        self.assertIsNone(building_type.description)
        self.assertIsNone(building_type.created_at)
        self.assertIsNone(building_type.updated_at)


class TestBuildingsTypesExceptions(unittest.TestCase):
    """Test cases for BuildingsTypes exceptions."""

    def test_building_type_not_found_exception(self):
        """Test BuildingTypeNotFoundException."""
        from chalicelib.dddpy.core_buildings_types.domain.buildings_types_exception import (
            BuildingTypeNotFoundException
        )
        
        exc = BuildingTypeNotFoundException()
        self.assertEqual(exc.message, "Building type not found")
        self.assertEqual(exc.status_code, 404)

    def test_building_type_already_exists_exception(self):
        """Test BuildingTypeAlreadyExistsException."""
        from chalicelib.dddpy.core_buildings_types.domain.buildings_types_exception import (
            BuildingTypeAlreadyExistsException
        )
        
        exc = BuildingTypeAlreadyExistsException()
        self.assertEqual(exc.message, "Building type already exists")
        self.assertEqual(exc.status_code, 409)


class TestBuildingsTypesSuccessMessages(unittest.TestCase):
    """Test cases for BuildingsTypes success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_buildings_types.domain.buildings_types_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.BUILDING_TYPE_CREATED, "Building type created successfully")
        self.assertEqual(SuccessMessages.BUILDING_TYPE_UPDATED, "Building type updated successfully")
        self.assertEqual(SuccessMessages.BUILDING_TYPE_DELETED, "Building type deleted successfully")
        self.assertEqual(SuccessMessages.BUILDING_TYPE_RETRIEVED, "Building type retrieved successfully")
        self.assertEqual(SuccessMessages.BUILDING_TYPES_LISTED, "Building types listed successfully")


if __name__ == "__main__":
    unittest.main()
