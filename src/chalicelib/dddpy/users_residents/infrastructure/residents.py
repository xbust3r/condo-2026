from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from chalicelib.dddpy.shared.mysql.base import Base


class DBUsersResidents(Base):
    __tablename__ = "users_residents"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    condominium_id = Column(BigInteger, ForeignKey("core_condominiums.id"), nullable=True)
    building_id = Column(BigInteger, ForeignKey("core_buildings.id"), nullable=True)
    unity_id = Column(BigInteger, ForeignKey("core_unitys.id"), nullable=True)
    type = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True, default="active")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
