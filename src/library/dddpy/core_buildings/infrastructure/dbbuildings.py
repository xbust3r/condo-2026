from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, DateTime, func
from library.dddpy.shared.mysql.base import Base


class DBBuildings(Base):
    __tablename__ = 'core_buildings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    building_type_id = Column(BigInteger, nullable=True, index=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    built_area = Column(DECIMAL(12, 4), nullable=True)
    common_area = Column(DECIMAL(12, 4), nullable=True)
    coefficient = Column(DECIMAL(9, 6), nullable=True)
    floors_count = Column(Integer, nullable=False, server_default='0')
    basements_count = Column(Integer, nullable=False, server_default='0')
    units_planned = Column(Integer, nullable=False, server_default='0')
    sort_order = Column(Integer, nullable=False, server_default='0')
    status = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)