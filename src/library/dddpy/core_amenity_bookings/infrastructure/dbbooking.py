"""
SQLAlchemy model for core_amenity_bookings.
"""
from sqlalchemy import (
    Column, BigInteger, String, Text, Date, DateTime,
    Numeric, Boolean, ForeignKey, Index, func, JSON,
)

from library.dddpy.shared.mysql.base import Base


class DBBooking(Base):
    __tablename__ = 'core_amenity_bookings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    building_id = Column(BigInteger, nullable=False, index=True)
    amenity_id = Column(BigInteger, nullable=False, index=True)
    unit_id = Column(BigInteger, nullable=False, index=True)
    owner_id = Column(BigInteger, nullable=False, index=True)

    unit_number_snapshot = Column(String(50), nullable=True)
    owner_name_snapshot = Column(String(200), nullable=True)

    booking_date = Column(Date, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)

    status = Column(String(20), nullable=False, server_default='draft')

    booking_fee_amount = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    security_deposit_amount = Column(Numeric(12, 2), nullable=False, server_default='0.00')
    currency = Column(String(3), nullable=False, server_default='PEN')

    booking_fee_ar_id = Column(BigInteger, nullable=True)
    security_deposit_ar_id = Column(BigInteger, nullable=True)

    deposit_status = Column(String(20), nullable=False, server_default='not_required')

    notes = Column(Text, nullable=True)
    created_by = Column(BigInteger, nullable=True)

    # ── Policy / allocation (B1-B3) ──
    guest_count = Column(BigInteger, nullable=False, server_default='1')
    allocation_source = Column(String(30), nullable=False, server_default='DIRECT')
    waitlist_entry_id = Column(BigInteger, nullable=True)
    idempotency_key = Column(String(64), nullable=True)
    policy_snapshot_json = Column(JSON, nullable=True)
    allocation_reason_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
