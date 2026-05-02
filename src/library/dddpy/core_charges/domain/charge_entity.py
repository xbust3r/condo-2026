"""
Charge domain entity — DDD for condominium charges.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any


class ChargeEntity:
    """Entidad de dominio para un cargo del condominio."""

    VALID_STATUSES = {"active", "inactive", "expired"}
    VALID_SCOPES = {"unit", "building", "condominium"}
    VALID_DISTRIBUTION_MODES = {
        "fixed_unit_amount",
        "prorated_by_building_coefficient",
        "prorated_by_condominium_coefficient",
    }

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        charge_type_id: int,
        scope: str = "unit",
        unit_id: Optional[int] = None,
        building_id: Optional[int] = None,
        distribution_mode: str = "fixed_unit_amount",
        description: Optional[str] = None,
        amount: Decimal = Decimal("0.00"),
        currency: str = "PEN",
        is_recurrent: bool = False,
        period_pattern: Optional[str] = None,
        start_date: date = None,
        end_date: Optional[date] = None,
        status: str = "active",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched fields
        charge_type_code: Optional[str] = None,
        charge_type_name: Optional[str] = None,
        charge_type_is_global: Optional[bool] = None,
        condominium_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        building_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.charge_type_id = charge_type_id
        self.scope = scope
        self.unit_id = unit_id
        self.building_id = building_id
        self.distribution_mode = distribution_mode
        self.description = description
        self.amount = amount
        self.currency = currency
        self.is_recurrent = is_recurrent
        self.period_pattern = period_pattern
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.charge_type_code = charge_type_code
        self.charge_type_name = charge_type_name
        self.charge_type_is_global = charge_type_is_global
        self.condominium_name = condominium_name
        self.unit_code = unit_code
        self.building_name = building_name

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.scope not in self.VALID_SCOPES:
            raise ValueError(
                f"scope must be one of: {', '.join(sorted(self.VALID_SCOPES))}"
            )
        if self.distribution_mode not in self.VALID_DISTRIBUTION_MODES:
            raise ValueError(
                f"distribution_mode must be one of: {', '.join(sorted(self.VALID_DISTRIBUTION_MODES))}"
            )
        # Scope-FK consistency: required FKs present, prohibited FKs absent
        if self.scope == "unit":
            if self.unit_id is None:
                raise ValueError("unit_id is required when scope=unit")
            if self.building_id is not None:
                raise ValueError("building_id must be null when scope=unit")
        elif self.scope == "building":
            if self.building_id is None:
                raise ValueError("building_id is required when scope=building")
            if self.unit_id is not None:
                raise ValueError("unit_id must be null when scope=building")
        elif self.scope == "condominium":
            if self.unit_id is not None or self.building_id is not None:
                raise ValueError(
                    "unit_id and building_id must be null when scope=condominium"
                )
        if self.amount <= 0:
            raise ValueError("amount must be > 0")
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if self.is_recurrent and not self.period_pattern:
            raise ValueError("recurrent charges require a period_pattern")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "charge_type_id": self.charge_type_id,
            "scope": self.scope,
            "unit_id": self.unit_id,
            "building_id": self.building_id,
            "distribution_mode": self.distribution_mode,
            "description": self.description,
            "amount": float(self.amount),
            "currency": self.currency,
            "is_recurrent": self.is_recurrent,
            "period_pattern": self.period_pattern,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # Enrichment
            "charge_type_code": self.charge_type_code,
            "charge_type_name": self.charge_type_name,
            "charge_type_is_global": self.charge_type_is_global,
            "condominium_name": self.condominium_name,
            "unit_code": self.unit_code,
            "building_name": self.building_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == "active" and not self.is_deleted()
