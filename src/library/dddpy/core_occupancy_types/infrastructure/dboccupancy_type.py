"""
OccupancyType DB model — SQLAlchemy for core_occupancy_types table.
"""
from sqlalchemy import Column, BigInteger, String, Text, SmallInteger, Integer, DateTime, Boolean, func
from library.dddpy.shared.mysql.base import Base


class DBOccupancyType(Base):
    __tablename__ = 'core_occupancy_types'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scope = Column(String(20), nullable=False, server_default='system')
    condominium_id = Column(BigInteger, nullable=True, index=True)
    requires_authorization = Column(SmallInteger, nullable=False, server_default='0')
    allows_primary = Column(SmallInteger, nullable=False, server_default='1')
    is_active = Column(SmallInteger, nullable=False, server_default='1')
    sort_order = Column(Integer, nullable=False, server_default='0')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)