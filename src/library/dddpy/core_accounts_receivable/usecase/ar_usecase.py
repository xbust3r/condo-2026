"""
AccountsReceivable use case — orchestrates all AR operations.
"""
from typing import Optional

from library.dddpy.core_accounts_receivable.usecase.ar_cmd_usecase import (
    ARCmdUseCase,
    ar_cmd_usecase_factory,
)
from library.dddpy.core_accounts_receivable.usecase.ar_query_usecase import (
    ARQueryUseCase,
    ar_query_usecase_factory,
)
from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import (
    CreateARSchema,
    UpdateARSchema,
    RecordPaymentSchema,
)
from library.dddpy.core_accounts_receivable.domain.ar_data import (
    CreateARData,
    UpdateARData,
)
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity
from library.dddpy.core_accounts_receivable.domain.ar_exception import (
    ARNotFound,
    ARPaymentExceedsBalance,
)
from library.dddpy.core_accounts_receivable.domain.ar_success import ARSuccessMessage
from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import (
    UnitOccupancyQueryRepositoryImpl,
)
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ARUseCase")


class ARUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: ARCmdUseCase = ar_cmd_usecase_factory()
        self._query: ARQueryUseCase = ar_query_usecase_factory()
        self._charge_query = ChargeUseCase()
        self._occupancy_repo = UnitOccupancyQueryRepositoryImpl()
        logger.info("ARUseCase initialized")

    # ── Create single AR ─────────────────────────────────────────────────

    def create(self, data: CreateARSchema):
        logger.add_inside_method("create")
        from decimal import Decimal

        cmd_data = CreateARData(
            condominium_id=data.condominium_id,
            unit_id=data.unit_id,
            debtor_user_id=data.debtor_user_id,
            reference_code=data.reference_code,
            description=data.description,
            amount=Decimal(str(data.amount)),
            currency=data.currency,
            due_date=data.due_date,
            period=data.period,
            charge_id=data.charge_id,
        )
        entity = self._cmd.create(cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Generate AR from a global charge (batch) ─────────────────────────

    def generate_from_charge(self, charge_id: int, due_date, period: Optional[str] = None):
        """
        For a global charge (all units), generate one AR per active unit.
        The debtor is the primary occupant (is_primary=True) or owner of the unit.
        """
        logger.add_inside_method("generate_from_charge")

        charge = self._charge_query.get_by_id(charge_id)
        if not charge:
            raise ARNotFound(f"Charge id={charge_id} not found")

        charge_data = charge.data

        # Only generate for global (unit_id=null) active charges
        if charge_data.get("unit_id") is not None:
            raise ValueError("Only global charges can be batch-generated")

        if charge_data.get("status") != "active":
            raise ValueError("Only active charges can generate AR")

        from decimal import Decimal

        # Get all active units in the condominium
        from library.dddpy.core_units.infrastructure.unit_query_repository import (
            UnitQueryRepositoryImpl,
        )
        unit_repo = UnitQueryRepositoryImpl()
        units, _ = unit_repo.list_all(
            condominium_id=charge_data["condominium_id"],
            status="active",
            include_deleted=False,
            limit=1000,
        )

        entries = []
        for unit in units:
            # Find primary occupant or owner
            occupancies, _ = self._occupancy_repo.list_by_unit(
                unit_id=unit.id,
                is_primary=True,
                status="active",
                include_deleted=False,
                limit=1,
            )
            debtor_user_id = None
            if occupancies:
                debtor_user_id = occupancies[0].user_id
            else:
                # Fall back to ownership
                from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
                    UnitOwnershipQueryRepositoryImpl,
                )
                ownership_repo = UnitOwnershipQueryRepositoryImpl()
                ownerships, _ = ownership_repo.list_by_unit(
                    unit_id=unit.id,
                    status="active",
                    include_deleted=False,
                    limit=1,
                )
                if ownerships:
                    debtor_user_id = ownerships[0].user_id

            if debtor_user_id is None:
                logger.warning(f"No debtor found for unit {unit.id}, skipping")
                continue

            entries.append(CreateARData(
                condominium_id=charge_data["condominium_id"],
                unit_id=unit.id,
                debtor_user_id=debtor_user_id,
                reference_code=f"AR-CHG-{charge_id}-{unit.code}",
                description=charge_data.get("description") or f"Cargo {charge_data.get('charge_type_name', '')}",
                amount=Decimal(str(charge_data["amount"])),
                currency=charge_data.get("currency", "PEN"),
                due_date=due_date,
                period=period or charge_data.get("period_pattern"),
                charge_id=charge_id,
            ))

        entities = self._cmd.create_batch(entries)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.CREATED,
            data={
                "charge_id": charge_id,
                "ar_count": len(entities),
                "ars": [e.to_dict() for e in entities],
            },
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise ARNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise ARNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateARSchema):
        logger.add_inside_method("update")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ARNotFound()

        cmd_data = UpdateARData(
            description=data.description,
            due_date=data.due_date,
            status=data.status,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Payments ──────────────────────────────────────────────────────────

    def record_payment(self, id: int, data: RecordPaymentSchema):
        """
        Record a payment against an AR.
        Automatically updates AR status: pending→partial or overdue→partial,
        and to paid when paid_amount == amount.
        """
        logger.add_inside_method("record_payment")

        from decimal import Decimal
        entity = self._cmd.add_payment(id, float(data.amount))
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.PAYMENT_RECORDED,
            data={
                "ar": entity.to_dict(),
                "payment_registered": float(data.amount),
                "new_status": entity.status,
            },
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ARNotFound()
        self._cmd.soft_delete(id)
        fresh = self._query._get_by_id_any_status(id)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.DELETED,
            data={"id": id, "deleted_at": fresh.deleted_at if fresh else None},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        existing = self._query._get_by_id_any_status(id)
        if not existing:
            raise ARNotFound()
        self._cmd.restore(id)
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ARNotFound()
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message="AR hard deleted successfully",
            data={"id": id},
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        debtor_user_id: Optional[int] = None,
        status: Optional[str] = None,
        charge_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            unit_id=unit_id,
            debtor_user_id=debtor_user_id,
            status=status,
            charge_id=charge_id,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Overdue ─────────────────────────────────────────────────────────

    def list_overdue(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_overdue")
        entities, total = self._query.list_overdue(
            condominium_id=condominium_id,
            as_of_date=as_of_date,
            skip=skip,
            limit=limit,
        )
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.OVERDUE_MARKED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Unit Summary ──────────────────────────────────────────────────────

    def get_summary_by_unit(self, unit_id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_summary_by_unit")
        summary = self._query.get_summary_by_unit(unit_id)
        return ResponseSuccessSchema(
            success=True,
            message="AR summary retrieved",
            data=summary,
        )
