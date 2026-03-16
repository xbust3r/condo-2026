# Users Domain Entity
from typing import Optional
from datetime import datetime
import bcrypt


class Users:
    """Domain entity for User"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        password: Optional[str] = None,
        doc_identity: Optional[str] = None,
        phone: Optional[str] = None,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.doc_identity = doc_identity
        self.phone = phone
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def set_password(self, password: str):
        """Hash and set password"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password"""
        if not self.password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def activate(self):
        self.status = 1
        self.updated_at = datetime.now()

    def deactivate(self):
        self.status = 0
        self.updated_at = datetime.now()

    def suspend(self):
        self.status = 2
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "doc_identity": self.doc_identity,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UsersException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UsersNotFoundException(UsersException):
    def __init__(self, user_id: int = None):
        super().__init__(f"User with id {user_id} not found", status_code=404)


class UsersAlreadyExistsException(UsersException):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists", status_code=409)


class UsersRepository:
    
    def all(self):
        raise NotImplementedError
    
    def create(self, data: dict):
        raise NotImplementedError
    
    def update(self, id: int, data: dict):
        raise NotImplementedError
    
    def delete(self, id: int):
        raise NotImplementedError
    
    def get_by_id(self, id: int):
        raise NotImplementedError
    
    def get_by_email(self, email: str):
        raise NotImplementedError
