"""
Permission Mapper — DB model ↔ Domain entity.
"""
from library.dddpy.core_permissions.infrastructure.dbpermission import DBBPermissions
from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity


class PermissionMapper:
    """Mapper para convertir entre DBBPermissions y PermissionEntity."""

    @staticmethod
    def to_domain(db_permission: DBBPermissions) -> PermissionEntity:
        """Convierte modelo DB a entidad de dominio."""
        return PermissionEntity(
            id=db_permission.id,
            code=db_permission.code,
            resource=db_permission.resource,
            action=db_permission.action,
            scope_default=db_permission.scope_default,
            description=db_permission.description,
            created_at=db_permission.created_at,
        )
