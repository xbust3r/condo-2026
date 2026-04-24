"""
SQLAlchemy model for core_documents.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime

from library.dddpy.shared.mysql.base import Base


class DBDocument(Base):
    __tablename__ = 'core_documents'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    uploader_user_id = Column(BigInteger, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text(), nullable=True)
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=True)
    mime_type = Column(String(100), nullable=True)
    category = Column(String(30), nullable=False, server_default='other')
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)
