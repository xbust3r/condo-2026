"""
DB Permission Model — SQLAlchemy model for core_permissions table.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func

from library.dddpy.shared.mysql.base import Base


class DBBPermissions(Base):
    __tablename__ = 'core_permissions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    resource = Column(String(50), nullable=False, index=True)
    action = Column(String(30), nullable=False, index=True)
    scope_default = Column(String(20), nullable=False, server_default='condominium')
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
