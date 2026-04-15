"""
SQLAlchemy model for user_profiles table.

READS from the existing user_profiles table.
All writes go through UserProfileCmdRepository.
"""
from sqlalchemy import Column, BigInteger, String, Date, DateTime
from sqlalchemy.sql import func

from library.dddpy.shared.mysql.base import Base


class DBUserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    user_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    document_type = Column(String(20), nullable=True)
    document_number = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
