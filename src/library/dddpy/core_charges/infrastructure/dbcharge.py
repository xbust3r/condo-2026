"""
Charge DB model — SQLAlchemy for core_charges table.
"""
from sqlalchemy import Column, BigInteger, String, Text, SmallInteger, Date, DateTime, Numeric, func, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBCharge(Base):
    __tablename__ = 'core_charges'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_charges_condominium'),
        nullable=False,
        index=True,
    )
    charge_type_id = Column(
        BigInteger,
        ForeignKey('core_charge_types.id', name='fk_charges_charge_type'),
        nullable=False,
        index=True,
    )
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_charges_unit'),
        nullable=True,
        index=True,
    )
    description = Column(Text, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, server_default='PEN')
    is_recurrent = Column(SmallInteger, nullable=False, server_default='0')
    period_pattern = Column(String(7), nullable=True)  # 'YYYY-MM'
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, server_default='active')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
