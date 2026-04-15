from datetime import datetime, date
from typing import Optional, Dict, Any


class UnitOccupancyEntity:
    """Entidad de dominio para la ocupación de unidades inmobiliarias."""

    VALID_OCCUPANCY_TYPES = {"resident_owner", "tenant", "family_member", "office_user", "occasional_user"}
    VALID_STATUSES = {"active", "inactive", "historical", "pending"}

    def __init__(
        self,
        id: int,
        uuid: str,
        unit_id: int,
        user_id: int,
        occupancy_type: str,
        status: str,
        start_date: date,
        end_date: Optional[date] = None,
        is_primary: bool = False,
        authorized_by_user_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.unit_id = unit_id
        self.user_id = user_id
        self.occupancy_type = occupancy_type
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.is_primary = is_primary
        self.authorized_by_user_id = authorized_by_user_id
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.occupancy_type not in self.VALID_OCCUPANCY_TYPES:
            raise ValueError(
                f"occupancy_type must be one of: {', '.join(sorted(self.VALID_OCCUPANCY_TYPES))}"
            )
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "unit_id": self.unit_id,
            "user_id": self.user_id,
            "occupancy_type": self.occupancy_type,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_primary": self.is_primary,
            "authorized_by_user_id": self.authorized_by_user_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == "active" and not self.is_deleted()
