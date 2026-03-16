# Residents Domain Entity (Pivot table for User-Building-Unity relationship)
from typing import Optional
from datetime import datetime


class Residents:
    """Domain entity for Resident (pivot between User, Unity and Condominium)"""
    
    def __init__(
        self,
        id: int,
        condominium_id: int,
        building_id: int,
        unity_id: int,
        user_id: int,
        type: str,  # Owner, Tenant, Family, Employee
        status: int = 1,  # Active, Inactive, Historical
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.condominium_id = condominium_id
        self.building_id = building_id
        self.unity_id = unity_id
        self.user_id = user_id
        self.type = type
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "condominium_id": self.condominium_id,
            "building_id": self.building_id,
            "unity_id": self.unity_id,
            "user_id": self.user_id,
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ResidentsException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResidentsNotFoundException(ResidentsException):
    def __init__(self, resident_id: int = None):
        super().__init__(f"Resident with id {resident_id} not found", status_code=404)


class ResidentsAlreadyExistsException(ResidentsException):
    def __init__(self):
        super().__init__(f"Resident relationship already exists", status_code=409)


class ResidentsRepository:
    
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
    
    def get_by_user(self, user_id: int):
        raise NotImplementedError
    
    def get_by_unity(self, unity_id: int):
        raise NotImplementedError
