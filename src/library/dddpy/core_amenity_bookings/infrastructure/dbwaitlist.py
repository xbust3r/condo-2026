"""
ORM model for core_amenity_waitlist.

Waitlist lifecycle: WAITING → NOTIFIED → CONFIRMED/CONVERTED/EXPIRED/CANCELLED
"""
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from sqlalchemy import Column, BigInteger, String, Date, DateTime, Integer, Numeric, Text, JSON
from library.dddpy.shared.mysql.base import Base


class DBWaitlistEntry(Base):
    __tablename__ = 'core_amenity_waitlist'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    amenity_id = Column(BigInteger, nullable=False)
    unit_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    booking_date = Column(Date, nullable=False)
    requested_start_at = Column(DateTime, nullable=False)
    requested_end_at = Column(DateTime, nullable=False)
    guest_count = Column(Integer, nullable=False, default=1)
    status = Column(String(32), nullable=False, default='WAITING')
    priority_score_snapshot = Column(Numeric(16, 4), nullable=True)
    priority_reason_json = Column(JSON, nullable=True)
    effective_policy_snapshot_json = Column(JSON, nullable=True)
    idempotency_key = Column(String(255), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    notified_at = Column(DateTime, nullable=True)
    converted_booking_id = Column(BigInteger, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'amenity_id': self.amenity_id,
            'unit_id': self.unit_id,
            'user_id': self.user_id,
            'booking_date': self.booking_date.isoformat() if isinstance(self.booking_date, date) else str(self.booking_date),
            'requested_start_at': self.requested_start_at.isoformat() if isinstance(self.requested_start_at, datetime) else str(self.requested_start_at),
            'requested_end_at': self.requested_end_at.isoformat() if isinstance(self.requested_end_at, datetime) else str(self.requested_end_at),
            'guest_count': self.guest_count,
            'status': self.status,
            'priority_score_snapshot': float(self.priority_score_snapshot) if self.priority_score_snapshot else None,
            'priority_reason_json': self.priority_reason_json,
            'effective_policy_snapshot_json': self.effective_policy_snapshot_json,
            'idempotency_key': self.idempotency_key,
            'expires_at': self.expires_at.isoformat() if isinstance(self.expires_at, datetime) else None,
            'notified_at': self.notified_at.isoformat() if isinstance(self.notified_at, datetime) else None,
            'converted_booking_id': self.converted_booking_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else None,
        }
