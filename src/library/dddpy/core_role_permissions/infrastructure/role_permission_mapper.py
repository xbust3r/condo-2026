"""
RolePermission Mapper — DB model ↔ Domain entity.
"""
from library.dddpy.core_role_permissions.infrastructure.dbrolepermission import DBRolePermission
from library.dddpy.core_role_permissions.domain.role_permission_entity import RolePermissionEntity


class RolePermissionMapper:
    """Mapper para convertir entre DBRolePermission y RolePermissionEntity."""

    @staticmethod
    def to_domain(db_rp: DBRolePermission) -> RolePermissionEntity:
        """Convierte modelo DB a entidad de dominio."""
        return RolePermissionEntity(
            role=db_rp.role,
            permission_code=db_rp.permission_code,
            scope_override=db_rp.scope_override,
        )
