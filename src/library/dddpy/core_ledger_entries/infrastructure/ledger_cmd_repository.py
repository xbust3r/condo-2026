"""
Ledger command repository implementation — SQLAlchemy (append-only).
"""
from decimal import Decimal
from typing import Optional
import uuid as uuid_lib

from library.dddpy.core_ledger_entries.domain.ledger_cmd_repository import LedgerCmdRepository
from library.dddpy.core_ledger_entries.domain.ledger_data import CreateLedgerEntryData
from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity
from library.dddpy.core_ledger_entries.infrastructure.db_ledger import DBLedgerEntry
from library.dddpy.core_ledger_entries.infrastructure.ledger_mapper import LedgerMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("LedgerCmdRepository")


class LedgerCmdRepositoryImpl(LedgerCmdRepository):

    def __init__(self):
        logger.info("LedgerCmdRepositoryImpl initialized")

    def get_latest_balance(self, unit_id: int) -> float:
        with session_scope() as session:
            row = session.query(DBLedgerEntry).filter(
                DBLedgerEntry.unit_id == unit_id
            ).order_by(DBLedgerEntry.id.desc()).first()
            return float(row.balance) if row else 0.0

    def create(self, data: CreateLedgerEntryData) -> LedgerEntryEntity:
        logger.info(f"Appending ledger entry for unit={data.unit_id}, type={data.entry_type}")
        with session_scope() as session:
            # Get current balance
            last = session.query(DBLedgerEntry).filter(
                DBLedgerEntry.unit_id == data.unit_id
            ).order_by(DBLedgerEntry.id.desc()).first()
            current_balance = float(last.balance) if last else 0.0
            new_balance = current_balance + float(data.debit) - float(data.credit)

            db_le = DBLedgerEntry(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=data.condominium_id,
                unit_id=data.unit_id,
                entry_type=data.entry_type,
                ar_id=data.ar_id,
                payment_id=data.payment_id,
                charge_id=data.charge_id,
                description=data.description,
                debit=Decimal(str(data.debit)),
                credit=Decimal(str(data.credit)),
                balance=Decimal(str(round(new_balance, 2))),
                period=data.period,
                reference=data.reference,
            )
            session.add(db_le)
            session.flush()
            session.refresh(db_le)
            logger.info(f"Ledger entry created id={db_le.id}, new_balance={new_balance}")
            return LedgerMapper.to_domain(db_le)

    def create_batch(self, entries: list[CreateLedgerEntryData]) -> list[LedgerEntryEntity]:
        logger.info(f"Appending {len(entries)} ledger entries")
        with session_scope() as session:
            # Get current balance
            last = session.query(DBLedgerEntry).filter(
                DBLedgerEntry.unit_id == entries[0].unit_id
            ).order_by(DBLedgerEntry.id.desc()).first()
            current_balance = float(last.balance) if last else 0.0

            created = []
            for data in entries:
                new_balance = current_balance + float(data.debit) - float(data.credit)
                db_le = DBLedgerEntry(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    unit_id=data.unit_id,
                    entry_type=data.entry_type,
                    ar_id=data.ar_id,
                    payment_id=data.payment_id,
                    charge_id=data.charge_id,
                    description=data.description,
                    debit=Decimal(str(data.debit)),
                    credit=Decimal(str(data.credit)),
                    balance=Decimal(str(round(new_balance, 2))),
                    period=data.period,
                    reference=data.reference,
                )
                session.add(db_le)
                session.flush()
                session.refresh(db_le)
                current_balance = new_balance
                created.append(LedgerMapper.to_domain(db_le))

            logger.info(f"Batch ledger entries created: {len(created)}")
            return created
