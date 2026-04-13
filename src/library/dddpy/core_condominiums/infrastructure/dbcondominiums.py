from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, DateTime, func
from library.dddpy.shared.mysql.base import Base


class DBCondominiums(Base):
    __tablename__ = 'core_condominiums'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    legal_name = Column(String(255), nullable=True)
    document_number = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    land_area = Column(DECIMAL(12, 4), nullable=True)
    built_area = Column(DECIMAL(12, 4), nullable=True)
    area_unit = Column(String(20), default='m2')
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
