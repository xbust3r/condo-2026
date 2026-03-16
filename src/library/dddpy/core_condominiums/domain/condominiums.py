# Condominium Domain Entity
from typing import Optional
from datetime import datetime


class Condominium:
    """Domain entity for Condominium"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        size: Optional[float] = None,
        percentage: Optional[float] = None,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.size = size
        self.percentage = percentage
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def activate(self):
        self.status = 1
        self.updated_at = datetime.now()

    def deactivate(self):
        self.status = 0
        self.updated_at = datetime.now()

    def update(self, name: str = None, description: str = None, size: float = None, percentage: float = None):
        if name:
            self.name = name
        if description is not None:
            self.description = description
        if size is not None:
            self.size = size
        if percentage is not None:
            self.percentage = percentage
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "size": float(self.size) if self.size else None,
            "percentage": float(self.percentage) if self.percentage else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
