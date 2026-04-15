"""
Context use case — aggregates user context from multiple modules.

Provides a single API response with:
  - User identity (from core_users)
  - User profile (from core_user_profiles)
  - Unit ownerships (from core_unit_ownerships)
  - Unit occupancies (from core_unit_occupancies)
  - Condominium roles (from core_condominium_roles)

Used by:
  - GET /me/contexts     (current authenticated user)
  - GET /users/{id}/contexts  (admin view of any user)
"""
from typing import Any, Dict, List

from library.dddpy.core_users.infrastructure.user_query_repository import UserQueryRepositoryImpl
from library.dddpy.core_user_profiles.infrastructure.user_profile_query_repository import UserProfileQueryRepositoryImpl
from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import UnitOwnershipQueryRepositoryImpl
from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import UnitOccupancyQueryRepositoryImpl
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import CondominiumRoleQueryRepositoryImpl
from library.dddpy.core_units.infrastructure.unit_query_repository import UnitQueryRepositoryImpl
from library.dddpy.core_buildings.infrastructure.building_query_repository import BuildingQueryRepositoryImpl
from library.dddpy.core_users.domain.user_exception import UserNotFound
from library.dddpy.core_units.domain.unit_exception import UnitNotFound
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ContextUseCase")


class ContextUseCase:

    def __init__(self):
        self._user_query = UserQueryRepositoryImpl()
        self._profile_query = UserProfileQueryRepositoryImpl()
        self._ownership_query = UnitOwnershipQueryRepositoryImpl()
        self._occupancy_query = UnitOccupancyQueryRepositoryImpl()
        self._role_query = CondominiumRoleQueryRepositoryImpl()
        self._unit_query = UnitQueryRepositoryImpl()
        self._building_query = BuildingQueryRepositoryImpl()

    # ── User Context ─────────────────────────────────────────────────────────

    def get_user_context(self, user_id: int) -> Dict[str, Any]:
        """
        Aggregate full context for a user: identity + profile + ownerships + occupancies + roles.
        Raises UserNotFound if user does not exist.
        """
        # 1. User identity
        user = self._user_query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        # 2. Profile
        profile = self._profile_query.get_by_user_id(user_id)

        # 3. Ownerships (active only by default)
        ownerships, _ = self._ownership_query.list_by_user(
            user_id=user_id,
            status="active",
            include_deleted=False,
            limit=200,
        )

        # 4. Occupancies (active only by default)
        occupancies, _ = self._occupancy_query.list_by_user(
            user_id=user_id,
            status="active",
            include_deleted=False,
            limit=200,
        )

        # 5. Roles (active only by default)
        roles, _ = self._role_query.list_by_user(
            user_id=user_id,
            status="active",
            include_deleted=False,
            limit=200,
        )

        # Group roles by condominium
        roles_by_condominium: Dict[int, List[Dict]] = {}
        for role in roles:
            cond_id = role.condominium_id
            if cond_id not in roles_by_condominium:
                roles_by_condominium[cond_id] = []
            roles_by_condominium[cond_id].append(role.to_dict())

        return {
            "user": user.to_dict(),
            "profile": profile.to_dict() if profile else None,
            "ownerships": [o.to_dict() for o in ownerships],
            "occupancies": [o.to_dict() for o in occupancies],
            "roles_by_condominium": roles_by_condominium,
        }

    # ── Unit Summary ───────────────────────────────────────────────────────

    def get_unit_summary(self, unit_id: int) -> Dict[str, Any]:
        """
        Aggregate summary for a unit: unit data + building + ownerships + occupancies + resident count.
        Raises UnitNotFound if unit does not exist.
        """
        # 1. Unit
        unit = self._unit_query.get_by_id(unit_id)
        if not unit:
            raise UnitNotFound(f"Unit with id={unit_id} not found")

        # 2. Building
        building = self._building_query.get_by_id(unit.building_id) if unit.building_id else None

        # 3. Active ownerships
        ownerships, _ = self._ownership_query.list_by_unit(
            unit_id=unit_id,
            status="active",
            include_deleted=False,
            limit=200,
        )

        # 4. Active occupancies
        occupancies, _ = self._occupancy_query.list_by_unit(
            unit_id=unit_id,
            status="active",
            include_deleted=False,
            limit=200,
        )

        # 5. Active resident count
        resident_count = self._unit_query.count_active_residents(unit_id)

        return {
            "unit": unit.to_dict(),
            "building": building.to_dict() if building else None,
            "ownerships": [o.to_dict() for o in ownerships],
            "occupancies": [o.to_dict() for o in occupancies],
            "resident_count": resident_count,
        }
