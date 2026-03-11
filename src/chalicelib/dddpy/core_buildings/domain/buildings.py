from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.core_buildings.infrastructure.buildings import DBBuildings


class Buildings:
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        size: Optional[float] = None,
        percentage: Optional[float] = None,
        type: Optional[str] = None,
        condominium_id: Optional[int] = None,
        building_type_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.size = size
        self.percentage = percentage
        self.type = type
        self.condominium_id = condominium_id
        self.building_type_id = building_type_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_building: DBBuildings) -> 'Buildings':
        return cls(
            id=db_building.id,
            name=db_building.name,
            code=db_building.code,
            description=db_building.description,
            size=float(db_building.size) if db_building.size else None,
            percentage=float(db_building.percentage) if db_building.percentage else None,
            type=db_building.type,
            condominium_id=db_building.condominium_id,
            building_type_id=db_building.building_type_id,
            created_at=db_building.created_at,
            updated_at=db_building.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "size": self.size,
            "percentage": self.percentage,
            "type": self.type,
            "condominium_id": self.condominium_id,
            "building_type_id": self.building_type_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
