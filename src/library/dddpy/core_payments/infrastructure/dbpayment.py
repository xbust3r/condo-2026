"""
Payment DB model — SQLAlchemy for core_payments table.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Numeric, func, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBPayment(Base):
    __tablename__ = 'core_payments'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_payments_condominium'),
        nullable=False, index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_payments_unit'),
        nullable=False, index=True,
    )
    ar_id = Column(
        BigInteger,
        ForeignKey('core_accounts_receivable.id', name='fk_payments_ar'),
        nullable=False, index=True,
    )
    receipt_id = Column(
        BigInteger,
        ForeignKey('core_receipts.id', name='fk_payments_receipt'),
        nullable=True, index=True,
    )
    payer_user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_payments_payer'),
        nullable=False, index=True,
    )
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(30), nullable=False)
    reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
