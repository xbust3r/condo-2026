"""Unit tests for UsersResidents domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestUsersResidents(unittest.TestCase):
    """Test cases for UsersResidents domain class."""

    def test_users_residents_creation(self):
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
        
        self.assertEqual(resident.id, 1)
        self.assertEqual(resident.condominium_id, 1)
        self.assertEqual(resident.building_id, 1)
        self.assertEqual(resident.unity_id, 1)
        self.assertEqual(resident.type, "Propietario")
        self.assertEqual(resident.status, "vigente")
        self.assertEqual(resident.user_id, 1)

    def test_users_residents_to_dict(self):
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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["condominium_id"], 2)
        self.assertEqual(result["building_id"], 3)
        self.assertEqual(result["unity_id"], 4)
        self.assertEqual(result["type"], "Inquilino")
        self.assertEqual(result["status"], "vigente")
        self.assertEqual(result["user_id"], 5)
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_users_residents_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
        from chalicelib.dddpy.users_residents.infrastructure.residents import DBUsersResidents
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBUsersResidents)
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
        
        self.assertIsInstance(resident, UsersResidents)
        self.assertEqual(resident.id, 1)
        self.assertEqual(resident.condominium_id, 1)
        self.assertEqual(resident.building_id, 2)
        self.assertEqual(resident.unity_id, 3)
        self.assertEqual(resident.type, "Propietario")
        self.assertEqual(resident.status, "historico")
        self.assertEqual(resident.user_id, 4)

    def test_users_residents_optional_fields(self):
        """Test UsersResidents with optional fields as None."""
        from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
        
        resident = UsersResidents(
            id=1
        )
        
        self.assertIsNone(resident.condominium_id)
        self.assertIsNone(resident.building_id)
        self.assertIsNone(resident.unity_id)
        self.assertIsNone(resident.type)
        self.assertIsNone(resident.status)
        self.assertIsNone(resident.user_id)
        self.assertIsNone(resident.created_at)
        self.assertIsNone(resident.updated_at)

    def test_users_residents_resident_types(self):
        """Test UsersResidents with different resident types."""
        from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
        
        types = ["Propietario", "Inquilino", "Familiar", "Administrador"]
        
        for resident_type in types:
            resident = UsersResidents(
                id=1,
                type=resident_type,
                user_id=1
            )
            self.assertEqual(resident.type, resident_type)


class TestUsersResidentsExceptions(unittest.TestCase):
    """Test cases for UsersResidents exceptions."""

    def test_residents_not_found_exception(self):
        """Test ResidentsNotFoundException."""
        from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentsNotFoundException
        
        exc = ResidentsNotFoundException()
        self.assertEqual(exc.message, "Residents not found")
        self.assertEqual(exc.status_code, 404)

    def test_residents_already_exists_exception(self):
        """Test ResidentsAlreadyExistsException."""
        from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentsAlreadyExistsException
        
        exc = ResidentsAlreadyExistsException()
        self.assertEqual(exc.message, "Residents already exists")
        self.assertEqual(exc.status_code, 409)

    def test_residents_validation_exception(self):
        """Test ResidentsValidationException."""
        from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentsValidationException
        
        exc = ResidentsValidationException()
        self.assertEqual(exc.message, "Residents validation failed")
        self.assertEqual(exc.status_code, 400)


class TestUsersResidentsSuccessMessages(unittest.TestCase):
    """Test cases for UsersResidents success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.users_residents.domain.residents_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.RESIDENTS_CREATED, "Residents created successfully")
        self.assertEqual(SuccessMessages.RESIDENTS_UPDATED, "Residents updated successfully")
        self.assertEqual(SuccessMessages.RESIDENTS_DELETED, "Residents deleted successfully")
        self.assertEqual(SuccessMessages.RESIDENTS_RETRIEVED, "Residents retrieved successfully")
        self.assertEqual(SuccessMessages.RESIDENTS_LISTED, "Residents listed successfully")


if __name__ == "__main__":
    unittest.main()
