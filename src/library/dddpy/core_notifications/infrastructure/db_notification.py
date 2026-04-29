"""
SQLAlchemy model for core_notifications.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, JSON, Index

from library.dddpy.shared.mysql.base import Base


class DBNotification(Base):
    __tablename__ = 'core_notifications'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    channel = Column(String(20), nullable=False, server_default='in_app')
    type = Column(String(50), nullable=False)
    resource_type = Column(String(30), nullable=False)
    resource_id = Column(BigInteger, nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text(), nullable=True)
    is_read = Column(Boolean(), nullable=False, server_default='0')
    read_at = Column(DateTime(), nullable=True)
    meta_data = Column("metadata", JSON(), nullable=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)