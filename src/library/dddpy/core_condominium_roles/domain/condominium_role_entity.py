from datetime import datetime, date
from typing import Optional, Dict, Any


class CondominiumRoleEntity:
    """Entidad de dominio para asignaciones de rol en condominios."""

    VALID_ROLES = {
        "super_admin",
        "condominium_admin",
        "building_manager",
        "security_staff",
        "maintenance_staff",
        "support_staff",
    }

    VALID_STATUSES = {"active", "inactive", "historical"}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        user_id: int,
        role: str,
        status: str = "active",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.user_id = user_id
        self.role = role
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.role not in self.VALID_ROLES:
            raise ValueError(
                f"role must be one of: {', '.join(sorted(self.VALID_ROLES))}"
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
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == "active" and not self.is_deleted()
