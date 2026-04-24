from typing import Optional
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


class BuildingEntity:
    """Entidad de dominio para edificios/torres de un condominio."""

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        code: str,
        name: str,
        short_name: Optional[str] = None,
        description: Optional[str] = None,
        building_type_id: Optional[int] = None,
        built_area: Optional[Decimal] = None,
        common_area: Optional[Decimal] = None,
        coefficient: Optional[Decimal] = None,
        floors_count: int = 0,
        basements_count: int = 0,
        units_planned: int = 0,
        sort_order: int = 0,
        status: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.code = code
        self.name = name
        self.short_name = short_name
        self.description = description
        self.building_type_id = building_type_id
        self.built_area = built_area
        self.common_area = common_area
        self.coefficient = coefficient
        self.floors_count = floors_count
        self.basements_count = basements_count
        self.units_planned = units_planned
        self.sort_order = sort_order
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.built_area is not None and self.built_area < 0:
            raise ValueError("built_area must be >= 0")
        if self.common_area is not None and self.common_area < 0:
            raise ValueError("common_area must be >= 0")
        if self.coefficient is not None and (self.coefficient < 0 or self.coefficient > 100):
            raise ValueError("coefficient must be between 0 and 100")
        if self.floors_count < 0:
            raise ValueError("floors_count must be >= 0")
        if self.basements_count < 0:
            raise ValueError("basements_count must be >= 0")
        if self.units_planned < 0:
            raise ValueError("units_planned must be >= 0")
        if self.sort_order < 0:
            raise ValueError("sort_order must be >= 0")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "building_type_id": self.building_type_id,
            "code": self.code,
            "name": self.name,
            "short_name": self.short_name,
            "description": self.description,
            "built_area": float(self.built_area) if self.built_area else None,
            "common_area": float(self.common_area) if self.common_area else None,
            "coefficient": float(self.coefficient) if self.coefficient else None,
            "floors_count": self.floors_count,
            "basements_count": self.basements_count,
            "units_planned": self.units_planned,
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