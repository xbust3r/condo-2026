"""
SQLAlchemy model for core_announcements.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Index

from library.dddpy.shared.mysql.base import Base


class DBAnnouncement(Base):
    __tablename__ = 'core_announcements'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    author_user_id = Column(BigInteger, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text(), nullable=False)
    category = Column(String(20), nullable=False, server_default='info')
    visibility = Column(String(20), nullable=False, server_default='public')
    is_pinned = Column(Boolean(), nullable=False, server_default='0')
    tower_id = Column(BigInteger, nullable=True, index=True)
    published_at = Column(DateTime(), nullable=True)
    expires_at = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)
