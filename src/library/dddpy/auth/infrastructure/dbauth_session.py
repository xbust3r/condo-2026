"""
SQLAlchemy model for auth_sessions table.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func

from library.dddpy.shared.mysql.base import Base


class DBAuthSession(Base):
    __tablename__ = 'auth_sessions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False, index=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
