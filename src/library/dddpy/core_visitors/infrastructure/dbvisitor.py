"""SQLAlchemy model for core_visitors."""
from sqlalchemy import Column, BigInteger, String, DateTime, Date, Time, Text, Index

from library.dddpy.shared.mysql.base import Base


class DBVisitor(Base):
    __tablename__ = 'core_visitors'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    building_id = Column(BigInteger, nullable=True, index=True)
    unit_id = Column(BigInteger, nullable=False, index=True)
    host_user_id = Column(BigInteger, nullable=False, index=True)
    visitor_name = Column(String(150), nullable=False)
    visitor_document_type = Column(String(20), nullable=True)
    visitor_document_number = Column(String(50), nullable=True)
    visitor_phone = Column(String(30), nullable=True)
    expected_date = Column(Date(), nullable=False, index=True)
    expected_time = Column(Time(), nullable=False)
    actual_checkin_at = Column(DateTime(), nullable=True)
    actual_checkout_at = Column(DateTime(), nullable=True)
    status = Column(String(20), nullable=False, server_default='pending')
    visit_purpose = Column(String(30), nullable=False, server_default='other')
    access_code = Column(String(10), nullable=True)
    notes = Column(Text(), nullable=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)