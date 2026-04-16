"""
RolePermission Query Repository Implementation.
"""
from typing import List, Tuple

from library.dddpy.core_role_permissions.domain.role_permission_entity import RolePermissionEntity
from library.dddpy.core_role_permissions.domain.role_permission_query_repository import RolePermissionQueryRepository
from library.dddpy.core_role_permissions.infrastructure.dbrolepermission import DBRolePermission
from library.dddpy.core_role_permissions.infrastructure.role_permission_mapper import RolePermissionMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("RolePermissionQueryRepository")


class RolePermissionQueryRepositoryImpl(RolePermissionQueryRepository):

    def __init__(self) -> None:
        logger.info("RolePermissionQueryRepositoryImpl initialized")

    def list_by_role(self, role: str) -> List[RolePermissionEntity]:
        logger.debug(f"Listing permissions for role={role}")
        with session_scope() as session:
            results = session.query(DBRolePermission).filter(
                DBRolePermission.role == role
            ).all()
            return [RolePermissionMapper.to_domain(r) for r in results]

    def list_permissions_by_role(
        self, role: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[RolePermissionEntity], int]:
        logger.debug(f"Listing permissions for role={role} skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBRolePermission).filter(DBRolePermission.role == role)
            total = query.count()
            results = query.offset(skip).limit(limit).all()
            return [RolePermissionMapper.to_domain(r) for r in results], total

    def get_roles_for_permission(self, permission_code: str) -> List[str]:
        """Return list of role names that have the given permission."""
        logger.debug(f"Getting roles for permission={permission_code}")
        with session_scope() as session:
            results = session.query(DBRolePermission.role).filter(
                DBRolePermission.permission_code == permission_code
            ).all()
            return [r.role for r in results]
