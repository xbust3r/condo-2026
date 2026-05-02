from typing import Optional
from datetime import datetime, date
from typing import Optional, Dict, Any
from decimal import Decimal


class UnitOwnershipEntity:
    """Entidad de dominio para la propiedad/unidad de un usuario."""

    VALID_OWNERSHIP_TYPES = {"owner", "co_owner"}
    VALID_STATUSES = {"active", "inactive", "historical"}

    def __init__(
        self,
        id: int,
        uuid: str,
        unit_id: int,
        user_id: int,
        ownership_type: str,
        ownership_percentage: Decimal,
        status: str,
        start_date: date,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields (populated on query)
        unit_code: Optional[str] = None,
        building_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
        user_email: Optional[str] = None,
        user_full_name: Optional[str] = None,
        ownership_type_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.unit_id = unit_id
        self.user_id = user_id
        self.ownership_type = ownership_type
        self.ownership_percentage = ownership_percentage
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.unit_code = unit_code
        self.building_name = building_name
        self.condominium_name = condominium_name
        self.user_email = user_email
        self.user_full_name = user_full_name

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.ownership_type not in self.VALID_OWNERSHIP_TYPES:
            raise ValueError(
                f"ownership_type must be one of: {', '.join(sorted(self.VALID_OWNERSHIP_TYPES))}"
            )
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.ownership_percentage < 0 or self.ownership_percentage > 100:
            raise ValueError("ownership_percentage must be between 0 and 100")
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "unit_id": self.unit_id,
            "user_id": self.user_id,
            "ownership_type": self.ownership_type,
            "ownership_percentage": float(self.ownership_percentage) if self.ownership_percentage else None,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "unit_code": self.unit_code,
            "building_name": self.building_name,
            "condominium_name": self.condominium_name,
            "user_email": self.user_email,
            "user_full_name": self.user_full_name,
            "ownership_type": self.ownership_type,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == "active" and not self.is_deleted()
