"""
from typing import Optional
Ledger use case — unit financial ledger operations.
"""
from typing import Optional

from library.dddpy.core_ledger_entries.usecase.ledger_cmd_schema import CreateLedgerEntrySchema
from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity
from library.dddpy.core_ledger_entries.domain.ledger_exception import LedgerEntryNotFound
from library.dddpy.core_ledger_entries.domain.ledger_success import LedgerSuccessMessage
from library.dddpy.core_ledger_entries.infrastructure.ledger_cmd_repository import LedgerCmdRepositoryImpl
from library.dddpy.core_ledger_entries.infrastructure.ledger_query_repository import LedgerQueryRepositoryImpl
from library.dddpy.core_ledger_entries.domain.ledger_data import CreateLedgerEntryData
from library.dddpy.core_units.infrastructure.unit_query_repository import UnitQueryRepositoryImpl
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("LedgerUseCase")


class LedgerUseCase:

    def __init__(self):
        self._cmd = LedgerCmdRepositoryImpl()
        self._query = LedgerQueryRepositoryImpl()
        logger.info("LedgerUseCase initialized")

    def create(self, data: CreateLedgerEntrySchema) -> ResponseSuccessSchema:
        """
        Append a ledger entry to a unit's financial ledger.
        Balance is computed automatically (running balance).
        """
        logger.info(f"Creating ledger entry unit_id={data.unit_id}, type={data.entry_type}")

        # Get condominium_id from unit
        unit_repo = UnitQueryRepositoryImpl()
        unit = unit_repo.get_by_id(data.unit_id)
        if not unit:
            from library.dddpy.core_ledger_entries.domain.ledger_exception import LedgerEntryNotFound
            raise LedgerEntryNotFound(f"Unit id={data.unit_id} not found")

        entry_data = CreateLedgerEntryData(
            condominium_id=unit.condominium_id,
            unit_id=data.unit_id,
            entry_type=data.entry_type,
            ar_id=data.ar_id,
            payment_id=data.payment_id,
            charge_id=data.charge_id,
            description=data.description,
            debit=data.debit,
            credit=data.credit,
            period=data.period,
            reference=data.reference,
        )

        entry = self._cmd.create(entry_data)
        return ResponseSuccessSchema(
            success=True,
            message=LedgerSuccessMessage.ENTRY_CREATED,
            data=entry.to_dict(),
        )

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        entry = self._query.get_by_id(id)
        if not entry:
            raise LedgerEntryNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=LedgerSuccessMessage.RETRIEVED,
            data=entry.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        entry = self._query.get_by_uuid(uuid)
        if not entry:
            raise LedgerEntryNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=LedgerSuccessMessage.RETRIEVED,
            data=entry.to_dict(),
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        """Get full ledger for a unit with running balance."""
        if limit > 500:
            limit = 500
        entries, total = self._query.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            period=period,
        )
        return ResponseSuccessSchema(
            success=True,
            message=LedgerSuccessMessage.LEDGER_RETRIEVED,
            data={
                "items": [e.to_dict() for e in entries],
                "total": total,
                "unit_id": unit_id,
                "skip": skip,
                "limit": limit,
                "period": period,
            },
        )

    def get_balance_summary(self, unit_id: int) -> ResponseSuccessSchema:
        """Get total debt, total paid, and current balance for a unit."""
        summary = self._query.get_balance_summary(unit_id)
        return ResponseSuccessSchema(
            success=True,
            message="Balance summary retrieved successfully",
            data=summary,
        )

    def create_batch(
        self, entries: list[CreateLedgerEntrySchema]
    ) -> ResponseSuccessSchema:
        """Append multiple ledger entries at once (atomic)."""
        logger.info(f"Creating batch of {len(entries)} ledger entries")

        if not entries:
            return ResponseSuccessSchema(
                success=True,
                message="No entries to create",
                data={"items": [], "total": 0},
            )

        # Get first entry's unit to find condominium
        unit_repo = UnitQueryRepositoryImpl()
        unit = unit_repo.get_by_id(entries[0].unit_id)
        if not unit:
            raise LedgerEntryNotFound(f"Unit id={entries[0].unit_id} not found")

        data_list = []
        for e in entries:
            data_list.append(CreateLedgerEntryData(
                condominium_id=unit.condominium_id,
                unit_id=e.unit_id,
                entry_type=e.entry_type,
                ar_id=e.ar_id,
                payment_id=e.payment_id,
                charge_id=e.charge_id,
                description=e.description,
                debit=e.debit,
                credit=e.credit,
                period=e.period,
                reference=e.reference,
            ))

        created = self._cmd.create_batch(data_list)
        return ResponseSuccessSchema(
            success=True,
            message=f"{len(created)} ledger entries created",
            data={
                "items": [c.to_dict() for c in created],
                "total": len(created),
            },
        )
