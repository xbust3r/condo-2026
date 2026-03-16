# Unit Types Domain Entity
from typing import Optional
from datetime import datetime


class UnittysTypes:
    """Domain entity for Unity Type"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UnittysTypesException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UnittysTypesNotFoundException(UnittysTypesException):
    def __init__(self, type_id: int = None):
        super().__init__(f"Unity Type with id {type_id} not found", status_code=404)


class UnittysTypesAlreadyExistsException(UnittysTypesException):
    def __init__(self, code: str):
        super().__init__(f"Unity Type with code '{code}' already exists", status_code=409)


class UnittysTypesRepository:
    
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
    
    def get_by_code(self, code: str):
        raise NotImplementedError
