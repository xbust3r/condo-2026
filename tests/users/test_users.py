"""Unit tests for Users domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestUsers(unittest.TestCase):
    """Test cases for Users domain class."""

    def test_users_creation(self):
        """Test creating a Users instance."""
        from chalicelib.dddpy.users.domain.users import Users
        
        now = datetime.now()
        user = Users(
            id=1,
            first_name="Juan",
            last_name="Perez",
            email="juan.perez@example.com",
            password="hashed_password",
            doc_identity="12345678",
            phone="+1234567890",
            status="activo",
            created_at=now,
            updated_at=now
        )
        
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, "Juan")
        self.assertEqual(user.last_name, "Perez")
        self.assertEqual(user.email, "juan.perez@example.com")
        self.assertEqual(user.password, "hashed_password")
        self.assertEqual(user.doc_identity, "12345678")
        self.assertEqual(user.phone, "+1234567890")
        self.assertEqual(user.status, "activo")

    def test_users_to_dict(self):
        """Test to_dict method returns correct dictionary."""
        from chalicelib.dddpy.users.domain.users import Users
        
        now = datetime(2025, 1, 1, 12, 0, 0)
        user = Users(
            id=1,
            first_name="Maria",
            last_name="Garcia",
            email="maria.garcia@example.com",
            password="hashed_password",
            doc_identity="87654321",
            phone="+1987654321",
            status="activo",
            created_at=now,
            updated_at=now
        )
        
        result = user.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["first_name"], "Maria")
        self.assertEqual(result["last_name"], "Garcia")
        self.assertEqual(result["email"], "maria.garcia@example.com")
        self.assertEqual(result["doc_identity"], "87654321")
        self.assertEqual(result["phone"], "+1987654321")
        self.assertEqual(result["status"], "activo")
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_users_to_dict_excludes_password(self):
        """Test to_dict method excludes password for security."""
        from chalicelib.dddpy.users.domain.users import Users
        
        user = Users(
            id=1,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="secret_password"
        )
        
        result = user.to_dict()
        
        self.assertNotIn("password", result)
        self.assertNotIn("password", result.keys())

    def test_users_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.users.domain.users import Users
        from chalicelib.dddpy.users.infrastructure.users import DBUsers
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBUsers)
        mock_db.id = 1
        mock_db.first_name = "Carlos"
        mock_db.last_name = "Lopez"
        mock_db.email = "carlos.lopez@example.com"
        mock_db.password = "hashed_pwd"
        mock_db.doc_identity = "11223344"
        mock_db.phone = "+5511223344"
        mock_db.status = "inactivo"
        mock_db.created_at = now
        mock_db.updated_at = now
        
        user = Users.from_db(mock_db)
        
        self.assertIsInstance(user, Users)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, "Carlos")
        self.assertEqual(user.last_name, "Lopez")
        self.assertEqual(user.email, "carlos.lopez@example.com")

    def test_users_optional_fields(self):
        """Test Users with optional fields as None."""
        from chalicelib.dddpy.users.domain.users import Users
        
        user = Users(
            id=1,
            first_name="Minimal",
            last_name="User",
            email="minimal@example.com"
        )
        
        self.assertIsNone(user.password)
        self.assertIsNone(user.doc_identity)
        self.assertIsNone(user.phone)
        self.assertIsNone(user.status)
        self.assertIsNone(user.created_at)
        self.assertIsNone(user.updated_at)


class TestUsersExceptions(unittest.TestCase):
    """Test cases for Users exceptions."""

    def test_users_not_found_exception(self):
        """Test UsersNotFoundException."""
        from chalicelib.dddpy.users.domain.users_exception import UsersNotFoundException
        
        exc = UsersNotFoundException()
        self.assertEqual(exc.message, "Users not found")
        self.assertEqual(exc.status_code, 404)

    def test_users_already_exists_exception(self):
        """Test UsersAlreadyExistsException."""
        from chalicelib.dddpy.users.domain.users_exception import UsersAlreadyExistsException
        
        exc = UsersAlreadyExistsException()
        self.assertEqual(exc.message, "Users already exists")
        self.assertEqual(exc.status_code, 409)

    def test_users_validation_exception(self):
        """Test UsersValidationException."""
        from chalicelib.dddpy.users.domain.users_exception import UsersValidationException
        
        exc = UsersValidationException()
        self.assertEqual(exc.message, "Users validation failed")
        self.assertEqual(exc.status_code, 400)


class TestUsersSuccessMessages(unittest.TestCase):
    """Test cases for Users success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.users.domain.users_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.USERS_CREATED, "Users created successfully")
        self.assertEqual(SuccessMessages.USERS_UPDATED, "Users updated successfully")
        self.assertEqual(SuccessMessages.USERS_DELETED, "Users deleted successfully")
        self.assertEqual(SuccessMessages.USERS_RETRIEVED, "Users retrieved successfully")
        self.assertEqual(SuccessMessages.USERS_LISTED, "Users listed successfully")


if __name__ == "__main__":
    unittest.main()
