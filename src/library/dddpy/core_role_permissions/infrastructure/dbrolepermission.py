"""
DB RolePermission Model — SQLAlchemy model for core_role_permissions table.
"""
from sqlalchemy import Column, String, ForeignKey

from library.dddpy.shared.mysql.base import Base


class DBRolePermission(Base):
    __tablename__ = 'core_role_permissions'

    role = Column(
        String(40),
        nullable=False,
        primary_key=True,
    )
    permission_code = Column(
        String(100),
        ForeignKey('core_permissions.code', name='fk_role_permissions_permission', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )
    scope_override = Column(String(20), nullable=True)
