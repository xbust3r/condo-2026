"""
LedgerEntry DB model — SQLAlchemy for core_ledger_entries table.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Numeric, func, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBLedgerEntry(Base):
    __tablename__ = 'core_ledger_entries'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_ledger_condominium'),
        nullable=False, index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_ledger_unit'),
        nullable=False, index=True,
    )
    entry_type = Column(String(20), nullable=False)
    ar_id = Column(
        BigInteger,
        ForeignKey('core_accounts_receivable.id', name='fk_ledger_ar'),
        nullable=True, index=True,
    )
    payment_id = Column(
        BigInteger,
        ForeignKey('core_payments.id', name='fk_ledger_payment'),
        nullable=True, index=True,
    )
    charge_id = Column(
        BigInteger,
        ForeignKey('core_charges.id', name='fk_ledger_charge'),
        nullable=True, index=True,
    )
    description = Column(Text, nullable=False)
    debit = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    credit = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    balance = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    period = Column(String(7), nullable=True)
    reference = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
