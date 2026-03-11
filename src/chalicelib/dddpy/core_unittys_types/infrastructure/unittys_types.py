from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from chalicelib.dddpy.shared.mysql.base import Base


class DBUnitysTypes(Base):
    __tablename__ = "core_unittys_types"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
