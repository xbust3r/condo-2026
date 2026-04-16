"""
Permission Service — RBAC permission checking engine.

Provides has_permission(), get_user_permissions(), and
get_effective_resident_context() based on role-permission mappings
stored in core_role_permissions.
"""
from typing import Optional

from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_mapper import CondominiumRoleMapper
from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_role_permissions.infrastructure.role_permission_query_repository import (
    RolePermissionQueryRepositoryImpl,
)
from library.dddpy.core_permissions.infrastructure.permission_query_repository import (
    PermissionQueryRepositoryImpl,
)
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import (
    UnitOccupancyQueryRepositoryImpl,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PermissionService")


class PermissionService:
    """
    Central service for RBAC permission checks.

    Workflow:
      1. Fetch user's active CondominiumRoleEntity for the target condominium
      2. Map role → list of (permission_code, scope_override) via core_role_permissions
      3. For each permission, resolve scope (override > default)
      4. Check if the requested resource+action exists in the user's permission set
      5. Verify scope alignment (condominium / unit / building)
    """

    def __init__(self) -> None:
        self._rp_repo = RolePermissionQueryRepositoryImpl()
        self._perm_repo = PermissionQueryRepositoryImpl()
        self._occupancy_repo = UnitOccupancyQueryRepositoryImpl()
        logger.info("PermissionService initialized")

    def _get_roles_for_user(
        self, user_id: int, condominium_id: int
    ) -> list[CondominiumRoleEntity]:
        """Return active roles for user in condominium."""
        logger.debug(f"Fetching active roles for user={user_id} in condominium={condominium_id}")
        with session_scope() as session:
            from sqlalchemy import and_
            db_roles = session.query(DBCondominiumRoles).filter(
                and_(
                    DBCondominiumRoles.user_id == user_id,
                    DBCondominiumRoles.condominium_id == condominium_id,
                    DBCondominiumRoles.status == "active",
                    DBCondominiumRoles.deleted_at.is_(None),
                )
            ).all()
            return [CondominiumRoleMapper.to_domain(r) for r in db_roles]

    def _resolve_scope(
        self,
        scope_override: Optional[str],
        scope_default: str,
    ) -> str:
        """Resolve effective scope: scope_override wins over scope_default."""
        return scope_override or scope_default

    def _scope_covers(
        self,
        effective_scope: str,
        target_id: Optional[int],
        context_id: Optional[int],
    ) -> bool:
        """
        Check if the effective scope is satisfied by the provided context.

        Scope rules:
          - global:      always satisfied
          - condominium: always satisfied when called within a condominium context
          - unit:        target_id must match context unit
          - building:    target_id must match context building
        """
        if effective_scope == "global":
            return True
        if effective_scope == "condominium":
            return True
        if effective_scope in ("unit", "building"):
            if target_id is None or context_id is None:
                return True  # Can't verify, allow
            return target_id == context_id
        return True

    def has_permission(
        self,
        user_id: int,
        condominium_id: int,
        resource: str,
        action: str,
        unit_id: Optional[int] = None,
        building_id: Optional[int] = None,
    ) -> bool:
        """
        Check if user has permission (resource, action) in the given condominium.

        Args:
            user_id:          ID of the user
            condominium_id:   ID of the condominium context
            resource:         Permission resource (e.g. 'building', 'finance')
            action:           Permission action (e.g. 'read', 'create')
            unit_id:          Unit context for unit-scoped permissions
            building_id:      Building context for building-scoped permissions

        Returns:
            True if the user has the permission, False otherwise.
        """
        logger.debug(
            f"has_permission user={user_id} condo={condominium_id} "
            f"resource={resource} action={action}"
        )

        roles = self._get_roles_for_user(user_id, condominium_id)
        if not roles:
            logger.debug(f"No active roles for user={user_id} in condominium={condominium_id}")
            return False

        permission_code = f"{resource}.{action}"

        for role_entity in roles:
            role = role_entity.role
            rp_list = self._rp_repo.list_by_role(role)

            for rp in rp_list:
                if rp.permission_code != permission_code:
                    continue

                perm = self._perm_repo.get_by_code(rp.permission_code)
                if not perm:
                    continue

                effective_scope = self._resolve_scope(rp.scope_override, perm.scope_default)

                # Determine which context ID to check against
                context_id: Optional[int] = None
                if effective_scope == "unit":
                    context_id = unit_id
                elif effective_scope == "building":
                    context_id = building_id

                if self._scope_covers(effective_scope, target_id=context_id, context_id=context_id):
                    logger.debug(f"Permission granted: {permission_code} via role={role}")
                    return True

        logger.debug(f"Permission denied: {permission_code} for user={user_id}")
        return False

    def get_user_permissions(
        self, user_id: int, condominium_id: int
    ) -> list:
        """
        Get all effective PermissionEntity objects for a user in a condominium.
        Combines all permissions from all active roles.
        """
        logger.debug(f"get_user_permissions user={user_id} condominium={condominium_id}")

        roles = self._get_roles_for_user(user_id, condominium_id)
        if not roles:
            return []

        seen_codes: set[str] = set()
        permissions: list = []

        for role_entity in roles:
            rp_list = self._rp_repo.list_by_role(role_entity.role)
            for rp in rp_list:
                if rp.permission_code in seen_codes:
                    continue
                seen_codes.add(rp.permission_code)
                perm = self._perm_repo.get_by_code(rp.permission_code)
                if perm:
                    permissions.append(perm)

        return permissions

    def get_effective_resident_context(
        self, user_id: int, unit_id: int
    ) -> Optional[dict]:
        """
        Calculate the effective resident context for a user in a unit.

        Checks core_unit_occupancies for a primary active occupancy of type
        'resident_owner' or 'tenant' and returns the resident context dict.
        """
        logger.debug(f"get_effective_resident_context user={user_id} unit={unit_id}")

        occ = self._occupancy_repo.get_active_by_unit_and_user(
            unit_id=unit_id, user_id=user_id
        )
        if not occ:
            return None

        if occ.occupancy_type not in ("resident_owner", "tenant"):
            return None

        return {
            "role": "resident",
            "scope": "unit",
            "unit_id": unit_id,
            "occupancy_type": occ.occupancy_type,
        }
