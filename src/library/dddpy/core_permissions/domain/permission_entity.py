"""
Permission Entity — Dominio para core_permissions.
"""
from datetime import datetime
from typing import Dict, Any


class PermissionEntity:
    """Entidad de dominio para permisos RBAC."""

    def __init__(
        self,
        id: int,
        code: str,
        resource: str,
        action: str,
        scope_default: str = "condominium",
        description: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.code = code
        self.resource = resource
        self.action = action
        self.scope_default = scope_default
        self.description = description
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "resource": self.resource,
            "action": self.action,
            "scope_default": self.scope_default,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
