from sqlalchemy import Column, BigInteger, String, DateTime, func
from chalicelib.dddpy.shared.mysql.base import Base


class DBUsers(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    doc_identity = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(String(50), nullable=True, default="active")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
