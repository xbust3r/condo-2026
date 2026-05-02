"""
from typing import Optional
Charge use case — orchestrates all charge operations.
"""
from typing import Optional

from library.dddpy.core_charges.usecase.charge_cmd_usecase import (
    ChargeCmdUseCase,
    charge_cmd_usecase_factory,
)
from library.dddpy.core_charges.usecase.charge_query_usecase import (
    ChargeQueryUseCase,
    charge_query_usecase_factory,
)
from library.dddpy.core_charges.usecase.charge_cmd_schema import (
    CreateChargeSchema,
    UpdateChargeSchema,
)
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.domain.charge_exception import (
    ChargeNotFound,
    ChargeAmountInvalid,
)
from library.dddpy.core_charges.domain.charge_success import ChargeSuccessMessage
from library.dddpy.core_charge_types.domain.charge_type_exception import ChargeTypeNotFound
from library.dddpy.core_charge_types.usecase.charge_type_usecase import ChargeTypeUseCase
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeUseCase")


class ChargeUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: ChargeCmdUseCase = charge_cmd_usecase_factory()
        self._query: ChargeQueryUseCase = charge_query_usecase_factory()
        self._charge_type_query = ChargeTypeUseCase()
        logger.info("ChargeUseCase initialized")

    def _validate_create(self, data: CreateChargeSchema) -> None:
        """Validate business rules before creating a charge."""
        if data.amount <= 0:
            raise ChargeAmountInvalid()
        if data.is_recurrent and not data.period_pattern:
            raise ValueError("Recurrent charges require period_pattern (YYYY-MM)")
        # Validate charge type exists
        ct = self._charge_type_query.get_by_id(data.charge_type_id)
        if not ct:
            raise ChargeTypeNotFound(f"ChargeType id={data.charge_type_id} not found")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateChargeSchema, generate_ar: bool = False):
        """
        Create a new charge.

        If generate_ar=True (used for recurrent charges), the caller is responsible
        for generating AR entries. This method returns the created charge entity
        along with a flag indicating AR generation is needed.
        """
        logger.add_inside_method("create")
        self._validate_create(data)

        from library.dddpy.core_charges.domain.charge_data import CreateChargeData
        from decimal import Decimal

        cmd_data = CreateChargeData(
            condominium_id=data.condominium_id,
            charge_type_id=data.charge_type_id,
            scope=data.scope,
            unit_id=data.unit_id,
            building_id=data.building_id,
            distribution_mode=data.distribution_mode,
            description=data.description,
            amount=Decimal(str(data.amount)),
            currency=data.currency,
            is_recurrent=data.is_recurrent,
            period_pattern=data.period_pattern,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
        )
        entity = self._cmd.create(cmd_data)
        message = ChargeSuccessMessage.CREATED
        needs_ar = data.is_recurrent and data.scope in ("building", "condominium")
        return ResponseSuccessSchema(
            success=True,
            message=message,
            data={
                "charge": entity.to_dict(),
                "ar_generation_needed": needs_ar,
            },
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise ChargeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise ChargeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateChargeSchema):
        logger.add_inside_method("update")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeNotFound()

        # Domain-level scope consistency: validate that the resulting state
        # (existing + patch) won't produce a hybrid invalid state.
        eff_scope = data.scope if data.scope is not None else existing.scope
        eff_unit_id = data.unit_id if data.unit_id is not None else (
            None if data.clear_unit_id else existing.unit_id
        )
        eff_building_id = data.building_id if data.building_id is not None else (
            None if data.clear_building_id else existing.building_id
        )
        self._validate_effective_scope(eff_scope, eff_unit_id, eff_building_id)

        from library.dddpy.core_charges.domain.charge_data import UpdateChargeData
        from decimal import Decimal

        cmd_data = UpdateChargeData(
            scope=data.scope,
            unit_id=data.unit_id,
            building_id=data.building_id,
            clear_unit_id=data.clear_unit_id,
            clear_building_id=data.clear_building_id,
            distribution_mode=data.distribution_mode,
            description=data.description,
            amount=Decimal(str(data.amount)) if data.amount is not None else None,
            is_recurrent=data.is_recurrent,
            period_pattern=data.period_pattern,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    @staticmethod
    def _validate_effective_scope(scope: str, unit_id, building_id) -> None:
        """Validate that scope + FK combination is valid (required FKs present, prohibited FKs absent)."""
        valid_scopes = {"unit", "building", "condominium"}
        if scope not in valid_scopes:
            raise ValueError(f"scope must be one of: {', '.join(sorted(valid_scopes))}")
        if scope == "unit":
            if unit_id is None:
                raise ValueError("unit_id is required when scope=unit")
            if building_id is not None:
                raise ValueError("building_id must be null when scope=unit")
        elif scope == "building":
            if building_id is None:
                raise ValueError("building_id is required when scope=building")
            if unit_id is not None:
                raise ValueError("unit_id must be null when scope=building")
        elif scope == "condominium":
            if unit_id is not None or building_id is not None:
                raise ValueError("unit_id and building_id must be null when scope=condominium")

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeNotFound()
        self._cmd.soft_delete(id)
        fresh = self._query._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        existing = self._query._get_by_id_any_status(id)
        if not existing:
            raise ChargeNotFound()
        self._cmd.restore(id)
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeNotFound()
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message="Charge hard deleted successfully",
            data={"id": id},
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        charge_type_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            charge_type_id=charge_type_id,
            unit_id=unit_id,
            status=status,
            is_recurrent=is_recurrent,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=ChargeSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )
