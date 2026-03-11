from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.core_unitys.infrastructure.unitys import DBUnitys


class Unitys:
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        size: Optional[float] = None,
        percentage: Optional[float] = None,
        type: Optional[str] = None,
        floor: Optional[int] = None,
        unit: Optional[str] = None,
        building_id: Optional[int] = None,
        unity_type_id: Optional[int] = None,
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
        self.floor = floor
        self.unit = unit
        self.building_id = building_id
        self.unity_type_id = unity_type_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_unity: DBUnitys) -> 'Unitys':
        return cls(
            id=db_unity.id,
            name=db_unity.name,
            code=db_unity.code,
            description=db_unity.description,
            size=float(db_unity.size) if db_unity.size else None,
            percentage=float(db_unity.percentage) if db_unity.percentage else None,
            type=db_unity.type,
            floor=db_unity.floor,
            unit=db_unity.unit,
            building_id=db_unity.building_id,
            unity_type_id=db_unity.unity_type_id,
            created_at=db_unity.created_at,
            updated_at=db_unity.updated_at
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
            "floor": self.floor,
            "unit": self.unit,
            "building_id": self.building_id,
            "unity_type_id": self.unity_type_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
