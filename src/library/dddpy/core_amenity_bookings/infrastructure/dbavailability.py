"""
SQLAlchemy model for core_amenity_availability_rules.

One row per amenity (UNIQUE on amenity_id).
"""
from sqlalchemy import (
    Column, BigInteger, String, Integer, Boolean, DateTime, Time, JSON, ForeignKey,
)

from library.dddpy.shared.mysql.base import Base


class DBAvailabilityRule(Base):
    __tablename__ = 'core_amenity_availability_rules'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    amenity_id = Column(BigInteger, ForeignKey('core_amenities.id'), nullable=False, unique=True)

    slot_mode = Column(String(20), nullable=False, default='CONTINUOUS_SLOTS')
    slot_interval_min = Column(Integer, nullable=True)
    window_start_time = Column(Time, nullable=True)
    window_end_time = Column(Time, nullable=True)

    max_capacity_per_slot = Column(Integer, nullable=False, default=1)

    advance_booking_days = Column(Integer, nullable=True)
    cancel_window_hours = Column(Integer, nullable=True)

    blocked_dates_json = Column(JSON, nullable=True)
    opening_hours_json = Column(JSON, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
