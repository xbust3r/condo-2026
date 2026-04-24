from sqlalchemy import Column, BigInteger, String, Text, Date, DateTime, Boolean, ForeignKey, func
from library.dddpy.shared.mysql.base import Base


class DBUnitOccupancy(Base):
    __tablename__ = 'core_unit_occupancies'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    unit_id = Column(
        BigInteger,
        ForeignKey('core_units.id', name='fk_unit_occupancies_unit'),
        nullable=False,
        index=True,
    )
    user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_unit_occupancies_user'),
        nullable=False,
        index=True,
    )
    occupancy_type_id = Column(
        BigInteger,
        ForeignKey('core_occupancy_types.id', name='fk_unit_occupancies_occupancy_type'),
        nullable=False,
        index=True,
    )
    status = Column(String(30), nullable=False, server_default='active')
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_primary = Column(Boolean, nullable=False, server_default='0')
    authorized_by_user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_unit_occupancies_authorizer'),
        nullable=True,
    )
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
