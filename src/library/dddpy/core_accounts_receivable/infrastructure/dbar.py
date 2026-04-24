"""
AccountsReceivable DB model — SQLAlchemy for core_accounts_receivable table.
"""
from sqlalchemy import Column, BigInteger, String, Text, SmallInteger, Date, DateTime, Numeric, func, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBAR(Base):
    __tablename__ = 'core_accounts_receivable'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_ar_condominium'),
        nullable=False,
        index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_ar_unit'),
        nullable=False,
        index=True,
    )
    debtor_user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_ar_debtor_user'),
        nullable=False,
        index=True,
    )
    reference_code = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    paid_amount = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    currency = Column(String(3), nullable=False, server_default='PEN')
    status = Column(String(20), nullable=False, server_default='pending', index=True)
    due_date = Column(Date, nullable=False)
    period = Column(String(7), nullable=True)  # 'YYYY-MM'
    charge_id = Column(
        BigInteger,
        ForeignKey('core_charges.id', name='fk_ar_charge'),
        nullable=True,
        index=True,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
