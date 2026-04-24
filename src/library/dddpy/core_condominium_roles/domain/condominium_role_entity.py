"""
from typing import Optional
Condominium Role Entity — Dominio para core_condominium_roles.

v2 — incluye scope y building_id desde migración 021.
"""
from datetime import datetime, date
from typing import Optional, Dict, Any


class CondominiumRoleEntity:
    """Entidad de dominio para asignaciones de rol en condominios."""

    VALID_ROLES: set[str] = {
        "super_admin",
        "condominium_admin",
        "board_member",
        "finance_reviewer",
        "security_staff",
        "maintenance_staff",
        "operations_staff",
    }

    VALID_SCOPES: set[str] = {"condominium", "unit", "building"}

    VALID_STATUSES: set[str] = {"active", "inactive", "historical"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        user_id: int,
        role: str,
        status: str = "active",
        scope: str = "condominium",
        building_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields (populated on query)
        user_full_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.user_id = user_id
        self.role = role
        self.status = status
        self.scope = scope
        self.building_id = building_id
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.user_full_name = user_full_name
        self.condominium_name = condominium_name

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.role not in self.VALID_ROLES:
            raise ValueError(
                f"role must be one of: {', '.join(sorted(self.VALID_ROLES))}"
            )
        if self.scope not in self.VALID_SCOPES:
            raise ValueError(
                f"scope must be one of: {', '.join(sorted(self.VALID_SCOPES))}"
            )
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date cannot be before start_date")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "user_id": self.user_id,
            "role": self.role,
            "status": self.status,
            "scope": self.scope,
            "building_id": self.building_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "user_full_name": self.user_full_name,
            "condominium_name": self.condominium_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == "active" and not self.is_deleted()
