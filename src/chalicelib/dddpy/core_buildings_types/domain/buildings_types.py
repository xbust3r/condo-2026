from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes


class BuildingsTypes:
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_building_type: DBBuildingsTypes) -> 'BuildingsTypes':
        return cls(
            id=db_building_type.id,
            name=db_building_type.name,
            code=db_building_type.code,
            description=db_building_type.description,
            created_at=db_building_type.created_at,
            updated_at=db_building_type.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
