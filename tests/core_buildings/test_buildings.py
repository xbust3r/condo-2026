"""Unit tests for Buildings domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestBuildings(unittest.TestCase):
    """Test cases for Buildings domain class."""

    def test_building_creation(self):
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
        
        self.assertEqual(building.id, 1)
        self.assertEqual(building.name, "Building A")
        self.assertEqual(building.code, "BLD-A")
        self.assertEqual(building.description, "Test building")
        self.assertEqual(building.size, 500.75)
        self.assertEqual(building.percentage, 2.5)
        self.assertEqual(building.type, "residential")
        self.assertEqual(building.condominium_id, 1)
        self.assertEqual(building.building_type_id, 1)

    def test_building_to_dict(self):
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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Building A")
        self.assertEqual(result["code"], "BLD-A")
        self.assertEqual(result["description"], "Test building")
        self.assertEqual(result["size"], 500.75)
        self.assertEqual(result["percentage"], 2.5)
        self.assertEqual(result["type"], "residential")
        self.assertEqual(result["condominium_id"], 1)
        self.assertEqual(result["building_type_id"], 1)
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_building_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
        from chalicelib.dddpy.core_buildings.infrastructure.buildings import DBBuildings
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBBuildings)
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
        
        self.assertIsInstance(building, Buildings)
        self.assertEqual(building.id, 1)
        self.assertEqual(building.name, "Building A")
        self.assertEqual(building.code, "BLD-A")

    def test_building_optional_fields(self):
        """Test Buildings with optional fields as None."""
        from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
        
        building = Buildings(
            id=1,
            name="Minimal Building",
            code="MB001"
        )
        
        self.assertIsNone(building.description)
        self.assertIsNone(building.size)
        self.assertIsNone(building.percentage)
        self.assertIsNone(building.type)
        self.assertIsNone(building.condominium_id)
        self.assertIsNone(building.building_type_id)
        self.assertIsNone(building.created_at)
        self.assertIsNone(building.updated_at)

    def test_building_size_conversion_from_db(self):
        """Test that size is properly converted from DB (string to float)."""
        from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
        from chalicelib.dddpy.core_buildings.infrastructure.buildings import DBBuildings
        
        mock_db = MagicMock(spec=DBBuildings)
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
        
        self.assertEqual(building.size, 500.75)
        self.assertEqual(building.percentage, 2.5)


class TestBuildingsExceptions(unittest.TestCase):
    """Test cases for Buildings exceptions."""

    def test_building_not_found_exception(self):
        """Test BuildingNotFoundException."""
        from chalicelib.dddpy.core_buildings.domain.buildings_exception import (
            BuildingNotFoundException
        )
        
        exc = BuildingNotFoundException()
        self.assertEqual(exc.message, "Building not found")
        self.assertEqual(exc.status_code, 404)

    def test_building_already_exists_exception(self):
        """Test BuildingAlreadyExistsException."""
        from chalicelib.dddpy.core_buildings.domain.buildings_exception import (
            BuildingAlreadyExistsException
        )
        
        exc = BuildingAlreadyExistsException()
        self.assertEqual(exc.message, "Building already exists")
        self.assertEqual(exc.status_code, 409)

    def test_building_validation_exception(self):
        """Test BuildingValidationException."""
        from chalicelib.dddpy.core_buildings.domain.buildings_exception import (
            BuildingValidationException
        )
        
        exc = BuildingValidationException()
        self.assertEqual(exc.message, "Building validation failed")
        self.assertEqual(exc.status_code, 400)


class TestBuildingsSuccessMessages(unittest.TestCase):
    """Test cases for Buildings success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_buildings.domain.buildings_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.BUILDING_CREATED, "Building created successfully")
        self.assertEqual(SuccessMessages.BUILDING_UPDATED, "Building updated successfully")
        self.assertEqual(SuccessMessages.BUILDING_DELETED, "Building deleted successfully")
        self.assertEqual(SuccessMessages.BUILDING_RETRIEVED, "Building retrieved successfully")
        self.assertEqual(SuccessMessages.BUILDINGS_LISTED, "Buildings listed successfully")


if __name__ == "__main__":
    unittest.main()
