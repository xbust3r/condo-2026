"""
SQLAlchemy model for core_amenities.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Numeric, ForeignKey, Index

from library.dddpy.shared.mysql.base import Base


class DBAmenity(Base):
    __tablename__ = 'core_amenities'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    scope = Column(String(20), nullable=False, default='CONDOMINIUM')
    building_id = Column(BigInteger, ForeignKey('core_buildings.id', ondelete='SET NULL'), nullable=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text(), nullable=True)
    location = Column(String(255), nullable=True)
    max_capacity = Column(BigInteger, nullable=False, server_default='1')
    booking_duration_min = Column(BigInteger, nullable=False, server_default='60')
    requires_approval = Column(Boolean(), nullable=False, server_default='0')
    booking_price = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    security_deposit_amount = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    amenity_type = Column(String(30), nullable=True)
    is_reservable = Column(Boolean(), nullable=False, server_default='0')
    status = Column(String(20), nullable=False, server_default='active')
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)

    __table_args__ = (
        Index('ix_amenities_condo_status', 'condominium_id', 'status'),
        Index('ix_amenities_scope_lookup', 'condominium_id', 'scope', 'building_id'),
    )
