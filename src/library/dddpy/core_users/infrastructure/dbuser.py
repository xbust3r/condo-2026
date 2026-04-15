"""
SQLAlchemy model for the users table.

This model READS from the existing users table.
All write operations go through UserCmdRepository.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Integer
from sqlalchemy.sql import func

from library.dddpy.shared.mysql.base import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)  # nullable for OAuth-only
    status = Column(String(20), nullable=False, server_default="active")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, nullable=False, server_default="0")
    locked_until = Column(DateTime, nullable=True)
    token_version = Column(Integer, nullable=False, server_default="0")
