from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


class UnitEntity:
    """Entidad de dominio para unidades inmobiliarias de un edificio."""

    VALID_OCCUPANCY_STATUSES = {
        "vacant",
        "occupied",
        "reserved",
        "maintenance",
        "blocked",
    }

    def __init__(
        self,
        id: int,
        uuid: str,
        building_id: int,
        unit_type_id: Optional[int] = None,
        unit_number: Optional[str] = None,
        code: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        private_area: Optional[Decimal] = None,
        coefficient: Optional[Decimal] = None,
        floor_number: Optional[int] = None,
        floor_label: Optional[str] = None,
        occupancy_status: str = "vacant",
        sort_order: int = 0,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.building_id = building_id
        self.unit_type_id = unit_type_id
        self.unit_number = unit_number
        self.code = code
        self.name = name
        self.description = description
        self.private_area = private_area
        self.coefficient = coefficient
        self.floor_number = floor_number
        self.floor_label = floor_label
        self.occupancy_status = occupancy_status
        self.sort_order = sort_order
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.private_area is not None and self.private_area < 0:
            raise ValueError("private_area must be >= 0")
        if self.coefficient is not None and (self.coefficient < 0 or self.coefficient > 100):
            raise ValueError("coefficient must be between 0 and 100")
        if self.sort_order < 0:
            raise ValueError("sort_order must be >= 0")
        if self.occupancy_status not in self.VALID_OCCUPANCY_STATUSES:
            raise ValueError(
                f"occupancy_status must be one of: {', '.join(sorted(self.VALID_OCCUPANCY_STATUSES))}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "building_id": self.building_id,
            "unit_type_id": self.unit_type_id,
            "unit_number": self.unit_number,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "private_area": float(self.private_area) if self.private_area else None,
            "coefficient": float(self.coefficient) if self.coefficient else None,
            "floor_number": self.floor_number,
            "floor_label": self.floor_label,
            "occupancy_status": self.occupancy_status,
            "sort_order": self.sort_order,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == 1 and not self.is_deleted()