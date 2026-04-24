"""SQLAlchemy model for core_packages."""
from sqlalchemy import Column, BigInteger, String, DateTime, Text, Index

from library.dddpy.shared.mysql.base import Base


class DBPackage(Base):
    __tablename__ = 'core_packages'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    unit_id = Column(BigInteger, nullable=False, index=True)
    recipient_user_id = Column(BigInteger, nullable=False, index=True)
    carrier = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    description = Column(Text(), nullable=True)
    status = Column(String(20), nullable=False, server_default='pending')
    received_at = Column(DateTime(), nullable=True)
    delivered_at = Column(DateTime(), nullable=True)
    pickup_code = Column(String(4), nullable=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)

    __table_args__ = (
        Index('ix_packages_condo_status', 'condominium_id', 'status'),
        Index('ix_packages_unit_status', 'unit_id', 'status'),
        Index('ix_packages_recipient', 'recipient_user_id'),
    )
