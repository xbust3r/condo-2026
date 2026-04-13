from datetime import datetime
from typing import Optional, Dict, Any


class CondominiumEntity:
    """Entidad de dominio para condominios."""

    def __init__(
        self,
        id: int,
        uuid: str,
        code: str,
        name: str,
        description: Optional[str] = None,
        size: Optional[float] = None,
        percentage: Optional[float] = None,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.code = code
        self.name = name
        self.description = description
        self.size = size
        self.percentage = percentage
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "size": float(self.size) if self.size else None,
            "percentage": float(self.percentage) if self.percentage else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }