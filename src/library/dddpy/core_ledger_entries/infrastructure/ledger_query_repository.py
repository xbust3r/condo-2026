"""
Ledger query repository implementation — SQLAlchemy.
"""
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import func

from library.dddpy.core_ledger_entries.domain.ledger_query_repository import LedgerQueryRepository
from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity
from library.dddpy.core_ledger_entries.infrastructure.db_ledger import DBLedgerEntry
from library.dddpy.core_ledger_entries.infrastructure.ledger_mapper import LedgerMapper
from library.dddpy.core_units.infrastructure.dbunits import DBUnits as DBUnit
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("LedgerQueryRepository")


class LedgerQueryRepositoryImpl(LedgerQueryRepository):

    def __init__(self):
        logger.info("LedgerQueryRepositoryImpl initialized")

    def _enrich(self, db_le: DBLedgerEntry, db_unit=None, db_condo=None) -> LedgerEntryEntity:
        entity = LedgerMapper.to_domain(db_le)
        if db_unit:
            entity.unit_code = db_unit.code
        if db_condo:
            entity.condominium_name = db_condo.name
        return entity

    def get_by_id(self, id: int) -> Optional[LedgerEntryEntity]:
        logger.info(f"Fetching ledger entry by id={id}")
        with session_scope() as session:
            row = session.query(DBLedgerEntry).filter(DBLedgerEntry.id == id).first()
            if not row:
                return None
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            return self._enrich(row, unit, condo)

    def get_by_uuid(self, uuid: str) -> Optional[LedgerEntryEntity]:
        logger.info(f"Fetching ledger entry by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBLedgerEntry).filter(DBLedgerEntry.uuid == uuid).first()
            if not row:
                return None
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            return self._enrich(row, unit, condo)

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
    ) -> Tuple[List[LedgerEntryEntity], int]:
        logger.info(f"Listing ledger for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBLedgerEntry).filter(DBLedgerEntry.unit_id == unit_id)
            if period:
                query = query.filter(DBLedgerEntry.period == period)

            total = query.count()
            rows = (
                query
                .order_by(DBLedgerEntry.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Enrich
            unit = session.query(DBUnit).filter(DBUnit.id == unit_id).first()
            condo = session.query(DBCondominium).filter(
                DBCondominium.id == rows[0].condominium_id
            ).first() if rows else None

            return [self._enrich(row, unit, condo) for row in rows], total

    def get_balance_summary(self, unit_id: int) -> dict:
        logger.info(f"Getting balance summary for unit_id={unit_id}")
        with session_scope() as session:
            result = session.query(
                func.sum(DBLedgerEntry.debit).label("total_debit"),
                func.sum(DBLedgerEntry.credit).label("total_credit"),
            ).filter(DBLedgerEntry.unit_id == unit_id).first()

            total_debit = float(result.total_debit or 0)
            total_credit = float(result.total_credit or 0)
            current_balance = total_debit - total_credit

            # Count overdue entries (charge entries with due_date in the past not fully paid)
            # For simplicity, we return counts by entry type
            charge_count = session.query(func.count(DBLedgerEntry.id)).filter(
                DBLedgerEntry.unit_id == unit_id,
                DBLedgerEntry.entry_type == "charge",
            ).scalar() or 0

            payment_count = session.query(func.count(DBLedgerEntry.id)).filter(
                DBLedgerEntry.unit_id == unit_id,
                DBLedgerEntry.entry_type == "payment",
            ).scalar() or 0

            return {
                "unit_id": unit_id,
                "total_debt": total_debit,
                "total_paid": total_credit,
                "current_balance": current_balance,
                "charge_count": charge_count,
                "payment_count": payment_count,
            }
