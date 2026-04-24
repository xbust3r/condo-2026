"""
LedgerEntry Mapper — transforms between DB model and domain entity.
"""
from library.dddpy.core_ledger_entries.infrastructure.db_ledger import DBLedgerEntry
from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity


class LedgerMapper:
    """Mapper para convertir entre DBLedgerEntry y LedgerEntryEntity."""

    @staticmethod
    def to_domain(db_le: DBLedgerEntry) -> LedgerEntryEntity:
        return LedgerEntryEntity(
            id=db_le.id,
            uuid=db_le.uuid,
            condominium_id=db_le.condominium_id,
            unit_id=db_le.unit_id,
            entry_type=db_le.entry_type,
            ar_id=db_le.ar_id,
            payment_id=db_le.payment_id,
            charge_id=db_le.charge_id,
            description=db_le.description,
            debit=db_le.debit,
            credit=db_le.credit,
            balance=db_le.balance,
            period=db_le.period,
            reference=db_le.reference,
            created_at=db_le.created_at,
        )

    @staticmethod
    def to_infrastructure(entity: LedgerEntryEntity) -> DBLedgerEntry:
        return DBLedgerEntry(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            unit_id=entity.unit_id,
            entry_type=entity.entry_type,
            ar_id=entity.ar_id,
            payment_id=entity.payment_id,
            charge_id=entity.charge_id,
            description=entity.description,
            debit=entity.debit,
            credit=entity.credit,
            balance=entity.balance,
            period=entity.period,
            reference=entity.reference,
            created_at=entity.created_at,
        )
