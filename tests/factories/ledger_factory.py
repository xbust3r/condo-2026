"""
Factory: LedgerEntry.

Creates test ledger entry records directly in the DB via SQLAlchemy.
"""
import uuid
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_ledger_entries.infrastructure.db_ledger import DBLedgerEntry


class LedgerFactory:
    """Factory for creating test LedgerEntry records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        entry_type: str = "charge",
        description: str = None,
        debit: Decimal = None,
        credit: Decimal = None,
        ar_id: int = None,
        payment_id: int = None,
        charge_id: int = None,
        **kwargs,
    ) -> DBLedgerEntry:
        db_ledger = DBLedgerEntry(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            unit_id=unit_id,
            entry_type=entry_type,
            ar_id=ar_id,
            payment_id=payment_id,
            charge_id=charge_id,
            description=description or "Factory-created ledger entry",
            debit=debit or Decimal("0.00"),
            credit=credit or Decimal("0.00"),
        )
        session.add(db_ledger)
        session.flush()
        session.refresh(db_ledger)
        return db_ledger
