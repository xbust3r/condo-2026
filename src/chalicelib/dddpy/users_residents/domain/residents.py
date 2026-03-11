from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.users_residents.infrastructure.residents import DBUsersResidents


class UsersResidents:
    def __init__(
        self,
        id: int,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        unity_id: Optional[int] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.condominium_id = condominium_id
        self.building_id = building_id
        self.unity_id = unity_id
        self.type = type
        self.status = status
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_resident: DBUsersResidents) -> 'UsersResidents':
        return cls(
            id=db_resident.id,
            condominium_id=db_resident.condominium_id,
            building_id=db_resident.building_id,
            unity_id=db_resident.unity_id,
            type=db_resident.type,
            status=db_resident.status,
            user_id=db_resident.user_id,
            created_at=db_resident.created_at,
            updated_at=db_resident.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "condominium_id": self.condominium_id,
            "building_id": self.building_id,
            "unity_id": self.unity_id,
            "type": self.type,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
