from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, DateTime, ForeignKey, func
from chalicelib.dddpy.shared.mysql.base import Base


class DBUnitys(Base):
    __tablename__ = "core_unitys"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    size = Column(DECIMAL(10, 2), nullable=True)
    percentage = Column(DECIMAL(5, 2), nullable=True)
    type = Column(String(100), nullable=True)
    floor = Column(Integer, nullable=True)
    unit = Column(String(50), nullable=True)
    building_id = Column(BigInteger, ForeignKey("core_buildings.id"), nullable=True)
    unity_type_id = Column(BigInteger, ForeignKey("core_unittys_types.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
