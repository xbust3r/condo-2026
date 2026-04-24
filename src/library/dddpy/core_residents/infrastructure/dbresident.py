"""
SQLAlchemy model for core_resident_profiles.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean

from library.dddpy.shared.mysql.base import Base


class DBResidentProfile(Base):
    __tablename__ = 'core_resident_profiles'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    user_id = Column(BigInteger, nullable=False)
    condominium_id = Column(BigInteger, nullable=False)
    notify_announcements = Column(Boolean(), nullable=False, server_default='1')
    notify_incidents = Column(Boolean(), nullable=False, server_default='1')
    notify_packages = Column(Boolean(), nullable=False, server_default='1')
    notify_visitors = Column(Boolean(), nullable=False, server_default='1')
    notify_payments = Column(Boolean(), nullable=False, server_default='1')
    language = Column(String(10), nullable=False, server_default='es')
    theme = Column(String(20), nullable=False, server_default='light')
    default_building_id = Column(BigInteger, nullable=True)
    notes = Column(Text(), nullable=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)
