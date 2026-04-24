"""
from typing import Optional
OccupancyType domain entity — DDD for unit occupancy type catalog.
"""
from datetime import datetime
from typing import Optional, Dict, Any


class OccupancyTypeEntity:
    """Entidad de dominio para el catálogo de tipos de ocupación."""

    def __init__(
        self,
        id: int,
        uuid: str,
        code: str,
        name: str,
        description: Optional[str] = None,
        scope: str = "system",
        condominium_id: Optional[int] = None,
        requires_authorization: bool = False,
        allows_primary: bool = True,
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
        self.scope = scope  # "system" | "condominium"
        self.condominium_id = condominium_id
        self.requires_authorization = requires_authorization
        self.allows_primary = allows_primary
        self.is_active = is_active
        self.sort_order = sort_order
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.sort_order < 0:
            raise ValueError("sort_order must be >= 0")
        if self.scope not in ("system", "condominium"):
            raise ValueError("scope must be 'system' or 'condominium'")
        if self.scope == "system" and self.condominium_id is not None:
            raise ValueError("system types must have condominium_id=null")
        if self.scope == "condominium" and self.condominium_id is None:
            raise ValueError("condominium types must have a valid condominium_id")

    @property
    def is_system(self) -> bool:
        return self.scope == "system"

    @property
    def is_custom(self) -> bool:
        return self.scope == "condominium"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "condominium_id": self.condominium_id,
            "requires_authorization": self.requires_authorization,
            "allows_primary": self.allows_primary,
            "is_active": self.is_active,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active_type(self) -> bool:
        return self.is_active and not self.is_deleted()