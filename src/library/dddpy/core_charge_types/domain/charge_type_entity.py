"""
ChargeType domain entity — DDD for charge type catalog.
"""
from datetime import datetime
from typing import Optional, Dict, Any


class ChargeTypeEntity:
    """Entidad de dominio para el catálogo de tipos de cargo."""

    def __init__(
        self,
        id: int,
        uuid: str,
        code: str,
        name: str,
        description: Optional[str] = None,
        is_global: bool = True,
        is_active: bool = True,
        sort_order: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.code = code
        self.name = name
        self.description = description
        self.is_global = is_global
        self.is_active = is_active
        self.sort_order = sort_order
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.sort_order < 0:
            raise ValueError("sort_order must be >= 0")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "is_global": self.is_global,
            "is_active": self.is_active,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active_type(self) -> bool:
        return self.is_active and not self.is_deleted()
