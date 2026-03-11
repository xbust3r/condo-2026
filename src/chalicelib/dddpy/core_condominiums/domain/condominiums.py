from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums

class Condominiums:
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        size: Optional[float] = None,
        percentage: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.size = size
        self.percentage = percentage
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_condominium: DBCondominiums) -> 'Condominiums':
        return cls(
            id=db_condominium.id,
            name=db_condominium.name,
            code=db_condominium.code,
            description=db_condominium.description,
            size=db_condominium.size,
            percentage=db_condominium.percentage,
            created_at=db_condominium.created_at,
            updated_at=db_condominium.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "size": self.size,
            "percentage": self.percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
