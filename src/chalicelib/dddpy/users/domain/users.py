from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.users.infrastructure.users import DBUsers


class Users:
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        password: Optional[str] = None,
        doc_identity: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.doc_identity = doc_identity
        self.phone = phone
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db(cls, db_user: DBUsers) -> 'Users':
        return cls(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            password=db_user.password,
            doc_identity=db_user.doc_identity,
            phone=db_user.phone,
            status=db_user.status,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "doc_identity": self.doc_identity,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
