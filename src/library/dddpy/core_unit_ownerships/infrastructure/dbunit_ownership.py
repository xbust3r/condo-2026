from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Date, DateTime, Integer, ForeignKey, ForeignKeyConstraint, func
from library.dddpy.shared.mysql.base import Base


class DBUnitOwnership(Base):
    __tablename__ = 'core_unit_ownerships'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    unit_id = Column(BigInteger, nullable=False, index=True, comment="FK to core_units.id")
    user_id = Column(BigInteger, nullable=False, index=True, comment="FK to users.id")
    ownership_type = Column(String(30), nullable=False, comment="owner or co_owner")
    ownership_percentage = Column(DECIMAL(5, 2), nullable=False, comment="Percentage 0-100")
    status = Column(String(30), nullable=False, server_default='active', comment="active/inactive/historical")
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(['unit_id'], ['core_units.id'], name='fk_unit_ownerships_unit'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_unit_ownerships_user'),
    )
