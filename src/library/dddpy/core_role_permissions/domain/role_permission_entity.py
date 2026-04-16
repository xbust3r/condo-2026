"""
RolePermission Entity — Dominio para core_role_permissions.
"""
from typing import Dict, Any, Optional


class RolePermissionEntity:
    """Entidad de dominio para asignaciones de permiso a rol."""

    def __init__(
        self,
        role: str,
        permission_code: str,
        scope_override: Optional[str] = None,
    ) -> None:
        self.role = role
        self.permission_code = permission_code
        self.scope_override = scope_override

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "permission_code": self.permission_code,
            "scope_override": self.scope_override,
        }
