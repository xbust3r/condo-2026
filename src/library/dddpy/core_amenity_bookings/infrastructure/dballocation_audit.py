"""
SQLAlchemy model for core_amenity_allocation_audit.
"""
from sqlalchemy import (
    Column, BigInteger, String, DateTime, JSON, ForeignKey, Index, func,
)

from library.dddpy.shared.mysql.base import Base


class DBAllocationAudit(Base):
    __tablename__ = 'core_amenity_allocation_audit'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    amenity_id = Column(BigInteger, ForeignKey('core_amenities.id'), nullable=False, index=True)
    booking_id = Column(BigInteger, nullable=True, index=True)
    waitlist_entry_id = Column(BigInteger, nullable=True)
    decision_type = Column(String(30), nullable=False)
    decision_reason = Column(String(255), nullable=True)
    decision_context_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    __table_args__ = (
        Index('idx_audit_amenity_date', 'amenity_id', 'created_at'),
        Index('idx_audit_decision_type', 'decision_type'),
    )
