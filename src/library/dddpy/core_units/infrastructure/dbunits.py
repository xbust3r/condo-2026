from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, DateTime, func
from library.dddpy.shared.mysql.base import Base


class DBUnits(Base):
    __tablename__ = 'core_units'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    building_id = Column(BigInteger, nullable=False, index=True)
    unit_type_id = Column(BigInteger, nullable=True, index=True)
    unit_number = Column(String(50), nullable=True)  # NOT NULL enforced at app layer (code fallback)
    code = Column(String(50), nullable=False)  # NOT NULL enforced at DB level
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    private_area = Column(DECIMAL(12, 4), nullable=True)
    coefficient = Column(DECIMAL(9, 6), nullable=True)
    floor_number = Column(Integer, nullable=True)
    floor_label = Column(String(30), nullable=True)
    occupancy_status = Column(String(30), nullable=False, server_default='vacant')
    sort_order = Column(Integer, nullable=False, server_default='0')
    condominium_coefficient = Column(DECIMAL(9, 6), nullable=True)
    status = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
