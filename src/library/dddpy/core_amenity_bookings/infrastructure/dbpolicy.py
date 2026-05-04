"""
SQLAlchemy model for core_amenity_policies.

Represents a single policy scope row:
- CONDOMINIUM   → global defaults for the condo
- AMENITY_TYPE  → overrides per amenity category (POOL, GRILL, etc.)
- AMENITY       → overrides for a specific amenity instance
"""
from sqlalchemy import (
    Column, BigInteger, String, Integer, Boolean, DateTime, JSON, ForeignKey, Index,
)

from library.dddpy.shared.mysql.base import Base


class DBPolicy(Base):
    __tablename__ = 'core_amenity_policies'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    condominium_id = Column(BigInteger, ForeignKey('core_condominiums.id'), nullable=False)
    scope_level = Column(String(20), nullable=False, default='CONDOMINIUM')
    amenity_type = Column(String(30), nullable=True)
    amenity_id = Column(BigInteger, ForeignKey('core_amenities.id'), nullable=True)

    eligibility_mode = Column(String(30), nullable=True, default=None)
    max_reservations_per_period = Column(Integer, nullable=True)
    period_unit = Column(String(10), nullable=True)
    period_value = Column(Integer, nullable=True)
    max_active_reservations = Column(Integer, nullable=True)
    max_guests = Column(Integer, nullable=True)

    priority_policy = Column(String(30), nullable=True, default=None)
    priority_window_unit = Column(String(10), nullable=True)
    priority_window_value = Column(Integer, nullable=True)

    waitlist_mode = Column(String(30), nullable=True, default=None)
    approval_mode = Column(String(30), nullable=True, default=None)

    extra_rules_json = Column(JSON, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
