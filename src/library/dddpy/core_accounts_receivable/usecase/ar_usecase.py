"""
from typing import Optional
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

    # ── Generate AR from a charge (batch, uses proration) ───────────────

    def generate_from_charge(self, charge_id: int, due_date, period: Optional[str] = None):
        """
        For a charge with scope=building or scope=condominium, generate
        one AR per affected unit with the correctly prorated amount.

        Uses ProrationUsecase to compute the per-unit allocation,
        then resolves debtor (occupant → owner) for each unit.
        """
        logger.add_inside_method("generate_from_charge")

        # Fetch charge entity (not dict) for proration
        from library.dddpy.core_charges.infrastructure.charge_query_repository import (
            ChargeQueryRepositoryImpl,
        )
        charge_repo = ChargeQueryRepositoryImpl()
        charge_entity = charge_repo.get_by_id(charge_id)
        if not charge_entity:
            raise ARNotFound(f"Charge id={charge_id} not found")

        if charge_entity.status != "active":
            raise ValueError("Only active charges can generate AR")

        # Validate scope is supported
        if charge_entity.scope not in ("unit", "building", "condominium"):
            raise ValueError(f"Unknown scope: '{charge_entity.scope}'")

        from decimal import Decimal

        # 1. Compute proration breakdown
        from library.dddpy.core_charges.usecase.proration_usecase import ProrationUsecase
        proration = ProrationUsecase()
        breakdown = proration.generate_breakdown(charge_entity)

        logger.info(
            f"Proration breakdown: {len(breakdown.entries)} entries, "
            f"omitted={breakdown.units_omitted}, residual={breakdown.residual_assigned}"
        )

        # 2. For each proration entry, resolve debtor and build AR data
        from library.dddpy.core_accounts_receivable.infrastructure.ar_query_repository import (
            ARQueryRepositoryImpl,
        )
        ar_query = ARQueryRepositoryImpl()
        eff_period = period or charge_entity.period_pattern

        entries = []
        skipped_no_debtor = 0
        skipped_duplicate = 0

        for entry in breakdown.entries:
            # FIN-10: Idempotency check — don't create duplicate ARs
            if eff_period and ar_query.exists_by_charge_period_unit(
                charge_id=charge_id,
                period=eff_period,
                unit_id=entry.unit_id,
            ):
                logger.warning(
                    f"AR already exists for charge={charge_id} "
                    f"period={eff_period} unit={entry.unit_id}, skipping"
                )
                skipped_duplicate += 1
                continue

            # FIN-09: Resolve debtor — occupant → owner → skip
            debtor_user_id = self._resolve_debtor(entry.unit_id)
            if debtor_user_id is None:
                logger.warning(f"No debtor found for unit {entry.unit_id}, skipping")
                skipped_no_debtor += 1
                continue

            entries.append(CreateARData(
                condominium_id=charge_entity.condominium_id,
                unit_id=entry.unit_id,
                debtor_user_id=debtor_user_id,
                reference_code=f"AR-CHG-{charge_id}-U{entry.unit_id}",
                description=charge_entity.description or f"Cargo {charge_entity.charge_type_name or ''}",
                amount=entry.amount,
                currency=charge_entity.currency,
                due_date=due_date,
                period=eff_period,
                charge_id=charge_id,
            ))

        if not entries:
            raise ValueError(
                f"No AR entries generated. {len(breakdown.entries)} total, "
                f"{skipped_no_debtor} no debtor, {skipped_duplicate} duplicates. "
                f"Check unit occupancy/ownership data."
            )

        # 3. Batch create ARs
        entities = self._cmd.create_batch(entries)
        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.CREATED,
            data={
                "charge_id": charge_id,
                "ar_count": len(entities),
                "skipped_no_debtor": skipped_no_debtor,
                "skipped_duplicate": skipped_duplicate,
                "units_omitted": breakdown.units_omitted,
                "residual_assigned": float(breakdown.residual_assigned),
                "ars": [e.to_dict() for e in entities],
            },
        )

    def _resolve_debtor(self, unit_id: int):
        """
        FIN-09: Resolve debtor for a unit.
        Priority: primary active occupant → active owner → None (skip with warning).
        """
        occupancies, _ = self._occupancy_repo.list_by_unit(
            unit_id=unit_id,
            is_primary=True,
            status="active",
            include_deleted=False,
            limit=1,
        )
        if occupancies:
            return occupancies[0].user_id

        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        ownership_repo = UnitOwnershipQueryRepositoryImpl()
        ownerships, _ = ownership_repo.list_by_unit(
            unit_id=unit_id,
            status="active",
            include_deleted=False,
            limit=1,
        )
        if ownerships:
            return ownerships[0].user_id

        return None

    # ── Recurrence ───────────────────────────────────────────────────────

    def generate_recurring(self, charge_id: int, due_date=None, up_to_month: Optional[str] = None):
        """
        FIN-11: Generate ARs for a recurrent charge across all periods
        from start_date to end_date (or current month if end_date is null).

        The pipeline decides HOW to generate (proration, debtor, idempotency);
        this method only decides WHEN to fire — one invocation per period.

        Args:
            charge_id: The recurrent charge to process
            due_date: Optional override for AR due_date (defaults to last day of period)
            up_to_month: Optional 'YYYY-MM' cap (defaults to current month)

        Returns:
            Aggregated response with per-period results
        """
        logger.add_inside_method("generate_recurring")

        from datetime import date, timedelta
        from calendar import monthrange

        from library.dddpy.core_charges.infrastructure.charge_query_repository import (
            ChargeQueryRepositoryImpl,
        )
        charge_repo = ChargeQueryRepositoryImpl()
        charge_entity = charge_repo.get_by_id(charge_id)
        if not charge_entity:
            raise ARNotFound(f"Charge id={charge_id} not found")

        if not charge_entity.is_recurrent:
            raise ValueError(f"Charge id={charge_id} is not recurrent")

        if charge_entity.status != "active":
            raise ValueError("Only active charges can generate AR")

        if not charge_entity.period_pattern:
            raise ValueError("Recurrent charge requires period_pattern")

        # Compute periods from start_date to end_date (or current month)
        periods = self._compute_periods(
            start_date=charge_entity.start_date,
            end_date=charge_entity.end_date,
            up_to_month=up_to_month,
        )

        logger.info(
            f"Generating recurring ARs for charge id={charge_id} "
            f"across {len(periods)} periods: {periods[0]} → {periods[-1]}"
        )

        results = []
        total_created = 0
        total_skipped_duplicate = 0
        total_skipped_no_debtor = 0

        for period in periods:
            # Compute due_date: last day of the period month
            year, month = int(period[:4]), int(period[5:7])
            _, last_day = monthrange(year, month)
            period_due_date = due_date or date(year, month, last_day)

            try:
                result = self.generate_from_charge(
                    charge_id=charge_id,
                    due_date=period_due_date,
                    period=period,
                )
                data = result.data
                total_created += data.get("ar_count", 0)
                total_skipped_duplicate += data.get("skipped_duplicate", 0)
                total_skipped_no_debtor += data.get("skipped_no_debtor", 0)
                results.append({
                    "period": period,
                    "status": "generated",
                    "ar_count": data.get("ar_count", 0),
                    "skipped_duplicate": data.get("skipped_duplicate", 0),
                    "skipped_no_debtor": data.get("skipped_no_debtor", 0),
                })
            except ValueError as e:
                # Period where all units were skipped (no debtor, etc.) — not fatal
                logger.warning(f"Period {period}: {e}")
                results.append({
                    "period": period,
                    "status": "skipped",
                    "reason": str(e),
                })

        return ResponseSuccessSchema(
            success=True,
            message=ARSuccessMessage.CREATED,
            data={
                "charge_id": charge_id,
                "periods_processed": len(periods),
                "periods_with_ar": len([r for r in results if r["status"] == "generated"]),
                "total_ar_created": total_created,
                "total_skipped_duplicate": total_skipped_duplicate,
                "total_skipped_no_debtor": total_skipped_no_debtor,
                "periods": results,
            },
        )

    @staticmethod
    def _compute_periods(
        start_date,
        end_date,
        up_to_month: Optional[str] = None,
    ):
        """
        Compute all 'YYYY-MM' periods from start_date to end_date.
        If end_date is None, goes up to up_to_month (defaults to current month).
        """
        from datetime import date

        # Determine end boundary
        if end_date:
            end_year, end_month = end_date.year, end_date.month
        elif up_to_month:
            end_year, end_month = int(up_to_month[:4]), int(up_to_month[5:7])
        else:
            today = date.today()
            end_year, end_month = today.year, today.month

        periods = []
        year, month = start_date.year, start_date.month

        while (year < end_year) or (year == end_year and month <= end_month):
            periods.append(f"{year:04d}-{month:02d}")
            month += 1
            if month > 12:
                month = 1
                year += 1

        return periods

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

    def get_summary_by_user(
        self, condominium_id: int, user_id: int
    ) -> ResponseSuccessSchema:
        """Get debt summary for a user across all their units in a condominium."""
        logger.add_inside_method("get_summary_by_user")
        summary = self._query.get_summary_by_user(condominium_id, user_id)
        return ResponseSuccessSchema(
            success=True,
            message="User AR summary retrieved",
            data=summary,
        )
