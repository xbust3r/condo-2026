"""
SQLAlchemy model for core_meetings.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Index

from library.dddpy.shared.mysql.base import Base


class DBMeeting(Base):
    __tablename__ = 'core_meetings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    meeting_type = Column(String(20), nullable=False, server_default='assembly')
    title = Column(String(200), nullable=False)
    description = Column(Text(), nullable=True)
    meeting_date = Column(DateTime(), nullable=False)
    location = Column(String(300), nullable=True)
    status = Column(String(20), nullable=False, server_default='scheduled')
    approved_at = Column(DateTime(), nullable=True)
    created_by_user_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)

    __table_args__ = (
        Index('ix_meetings_condo_date', 'condominium_id', 'meeting_date'),
        Index('ix_meetings_status', 'status'),
    )
