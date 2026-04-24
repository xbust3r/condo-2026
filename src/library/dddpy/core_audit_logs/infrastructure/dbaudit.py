"""
DBAuditLog — SQLAlchemy model for core_audit_logs table.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from library.dddpy.shared.mysql.base import Base


class DBAuditLog(Base):
    __tablename__ = 'core_audit_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    action = Column(String(20), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(BigInteger, nullable=False)
    resource_uuid = Column(String(36), nullable=False)
    old_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    created_at = Column(DateTime, nullable=False)