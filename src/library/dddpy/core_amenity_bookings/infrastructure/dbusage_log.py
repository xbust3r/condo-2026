"""
ORM model for core_amenity_usage_logs.

Operational usage tracking — separate from allocation_audit by design.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, BigInteger, String, DateTime, Text, JSON
from library.dddpy.shared.mysql.base import Base


class DBUsageLog(Base):
    __tablename__ = 'core_amenity_usage_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    booking_id = Column(BigInteger, nullable=False)
    amenity_id = Column(BigInteger, nullable=False)
    condominium_id = Column(BigInteger, nullable=False)
    unit_id = Column(BigInteger, nullable=True)
    owner_id = Column(BigInteger, nullable=True)
    event_type = Column(String(20), nullable=False)
    event_at = Column(DateTime, nullable=False)
    recorded_by = Column(BigInteger, nullable=True)
    source = Column(String(20), nullable=False, default='system')
    notes = Column(Text, nullable=True)
    event_context_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'booking_id': self.booking_id,
            'amenity_id': self.amenity_id,
            'condominium_id': self.condominium_id,
            'unit_id': self.unit_id,
            'owner_id': self.owner_id,
            'event_type': self.event_type,
            'event_at': self.event_at.isoformat() if isinstance(self.event_at, datetime) else str(self.event_at),
            'recorded_by': self.recorded_by,
            'source': self.source,
            'notes': self.notes,
            'event_context_json': self.event_context_json,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
        }
