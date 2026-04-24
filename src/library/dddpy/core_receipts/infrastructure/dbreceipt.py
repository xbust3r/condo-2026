"""
Receipt DB model — SQLAlchemy for core_receipts table.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Numeric, func, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBReceipt(Base):
    __tablename__ = 'core_receipts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_receipts_condominium'),
        nullable=False,
        index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_receipts_unit'),
        nullable=False,
        index=True,
    )
    ar_id = Column(
        BigInteger,
        ForeignKey('core_accounts_receivable.id', name='fk_receipts_ar'),
        nullable=False,
        index=True,
    )
    receipt_number = Column(String(30), nullable=False)
    issued_at = Column(DateTime, nullable=False)
    payer_user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_receipts_payer'),
        nullable=False,
        index=True,
    )
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(30), nullable=False)
    reference = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
