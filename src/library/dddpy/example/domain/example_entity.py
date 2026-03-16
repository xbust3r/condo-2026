from datetime import datetime
from typing import Optional, Dict, Any


class ExampleEntity:
    """Entidad de ejemplo para mostrar la estructura base de un módulo."""

    def __init__(
        self,
        id: int,
        code: str,
        name: str,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
