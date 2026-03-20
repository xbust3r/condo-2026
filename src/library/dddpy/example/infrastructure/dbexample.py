from sqlalchemy import Column, Integer, String, DateTime, func, Index
from library.dddpy.shared.postgresql.base import Base


class DBExample(Base):
    __tablename__ = 'core_example'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('ix_example_code', 'code', unique=True),
    )
