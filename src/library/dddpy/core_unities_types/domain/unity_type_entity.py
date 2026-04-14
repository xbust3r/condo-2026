from datetime import datetime
from typing import Optional, Dict, Any


class UnityTypeEntity:
    """Entidad de dominio para tipos de unidad inmobiliaria."""

    def __init__(
        self,
        id: int,
        uuid: str,
        code: str,
        name: str,
        description: Optional[str] = None,
        condominium_id: Optional[int] = None,
        is_system: bool = False,
        sort_order: int = 0,
        usage_class: Optional[str] = None,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.code = code
        self.name = name
        self.description = description
        self.condominium_id = condominium_id
        self.is_system = bool(is_system)
        self.sort_order = sort_order
        self.usage_class = usage_class
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.sort_order < 0:
            raise ValueError("sort_order must be >= 0")

    @property
    def is_global(self) -> bool:
        """True when this type is system-wide (not tied to a condominium)."""
        return self.condominium_id is None

    @property
    def is_custom(self) -> bool:
        """True when this type is custom (tied to a specific condominium)."""
        return self.condominium_id is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "condominium_id": self.condominium_id,
            "scope": "global" if self.is_global else "custom",
            "is_system": self.is_system,
            "sort_order": self.sort_order,
            "usage_class": self.usage_class,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == 1 and not self.is_deleted()

    def can_be_modified(self) -> bool:
        """System types cannot be modified or deleted by users."""
        return not self.is_system

    def can_be_deleted(self) -> bool:
        """System types cannot be hard-deleted."""
        return not self.is_system
