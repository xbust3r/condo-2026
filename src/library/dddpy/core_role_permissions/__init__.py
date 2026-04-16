"""core_role_permissions module."""
from library.dddpy.core_role_permissions.domain.role_permission_entity import RolePermissionEntity
from library.dddpy.core_role_permissions.domain.role_permission_exception import RoleNotFound
from library.dddpy.core_role_permissions.usecase.role_permission_factory import (
    role_permission_query_usecase_factory,
)
