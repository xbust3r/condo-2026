"""
DB Condominium Role Model — SQLAlchemy model for core_condominium_roles table.

Includes scope and building_id from migration 021.
"""
from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, func

from library.dddpy.shared.mysql.base import Base


class DBCondominiumRoles(Base):
    __tablename__ = 'core_condominium_roles'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey('core_condominiums.id', name='fk_condominium_roles_condominium'),
        nullable=False,
        index=True,
    )
    user_id = Column(
        BigInteger,
        ForeignKey('users.id', name='fk_condominium_roles_user'),
        nullable=False,
        index=True,
    )
    role = Column(String(40), nullable=False, index=True)
    status = Column(String(30), nullable=False, server_default='active', index=True)
    scope = Column(String(20), nullable=False, server_default='condominium')
    building_id = Column(BigInteger, ForeignKey('core_buildings.id', name='fk_condominium_roles_building', ondelete='SET NULL'), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
