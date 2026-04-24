"""
SQLAlchemy model for core_incidents.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Date, Index

from library.dddpy.shared.mysql.base import Base


class DBIncident(Base):
    __tablename__ = 'core_incidents'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    building_id = Column(BigInteger, nullable=True, index=True)
    unit_id = Column(BigInteger, nullable=False, index=True)
    reported_by_user_id = Column(BigInteger, nullable=False, index=True)
    assigned_to_user_id = Column(BigInteger, nullable=True, index=True)
    category = Column(String(40), nullable=False, server_default='other')
    priority = Column(String(20), nullable=False, server_default='medium')
    status = Column(String(30), nullable=False, server_default='pending')
    title = Column(String(150), nullable=False)
    description = Column(Text(), nullable=True)
    photos = Column(Text(), nullable=True)  # JSON stored as TEXT
    internal_notes = Column(Text(), nullable=True)
    resolution_notes = Column(Text(), nullable=True)
    scheduled_date = Column(Date(), nullable=True)
    completed_date = Column(Date(), nullable=True)
    is_escalated = Column(Boolean(), nullable=False, server_default='0')
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)
