from typing import Optional
from typing import Optional

from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import (
    CreateUnitOccupancySchema,
    UpdateUnitOccupancySchema,
)
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_cmd_repository import UnitOccupancyCmdRepository
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_data import CreateUnitOccupancyData, UpdateUnitOccupancyData
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import (
    OccupancyTypeNotFoundInCatalog,
    InvalidOccupancyStatus,
    PrimaryOccupancyConflict,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyCmdUseCase")


class UnitOccupancyCmdUseCase:

    VALID_STATUSES = {"active", "inactive", "historical", "pending"}

    def __init__(self, repository: UnitOccupancyCmdRepository):
        self.repository = repository
        logger.info("UnitOccupancyCmdUseCase initialized")

    def _get_occupancy_type_from_catalog(self, occupancy_type_id: int) -> dict:
        """Look up occupancy type from the catalog. Raises OccupancyTypeNotFoundInCatalog if not found/inactive."""
        from library.dddpy.core_occupancy_types.usecase.occupancy_type_usecase import OccupancyTypeUseCase
        try:
            ot_response = OccupancyTypeUseCase().get_by_id(occupancy_type_id)
            ot = ot_response.data  # get_by_id returns ResponseSuccessSchema
            if not ot.get("is_active"):
                raise OccupancyTypeNotFoundInCatalog(occupancy_type_id)
            return {
                "code": ot.get("code"),
                "name": ot.get("name"),
                "requires_authorization": ot.get("requires_authorization"),
                "allows_primary": ot.get("allows_primary"),
            }
        except Exception:
            raise OccupancyTypeNotFoundInCatalog(occupancy_type_id)

    def _validate_status(self, status: str) -> None:
        if status not in self.VALID_STATUSES:
            raise InvalidOccupancyStatus(status)

    def _validate_unit_exists(self, unit_id: int) -> None:
        """Validate unit exists and is active."""
        from library.dddpy.core_units.usecase.unit_usecase import UnitUseCase
        try:
            UnitUseCase().get_by_id(unit_id)
        except Exception:
            from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import UnitNotFoundForOccupancy
            raise UnitNotFoundForOccupancy()

    def _validate_user_exists(self, user_id: int) -> None:
        """Validate user exists."""
        from library.dddpy.core_users.usecase.user_usecase import UserUseCase
        try:
            UserUseCase().get_by_id(user_id)
        except Exception:
            from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import UserNotFoundForOccupancy
            raise UserNotFoundForOccupancy()

    def _check_primary_conflict(self, unit_id: int, exclude_id: Optional[int] = None) -> None:
        """Check if another primary occupancy exists for this unit."""
        existing = self.repository.find_primary_by_unit(unit_id)
        if existing and (exclude_id is None or existing.id != exclude_id):
            raise PrimaryOccupancyConflict()

    def _validate_authorized_by(self, authorized_by_user_id: Optional[int], unit_id: int) -> None:
        """
        Validate authorized_by_user_id if provided.

        Phase 1d: The authorizer must be either:
        1. An active owner of the unit (has active ownership_percentage > 0)
        2. Or have a role in the condominium that grants authorization rights
           (condominium_admin, board_member, super_admin)

        Raises UnauthorizedOccupancy if the authorizer is not valid.
        """
        if authorized_by_user_id is None:
            return

        # Check 1: Is this user an active owner of this unit?
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        ownership_repo = UnitOwnershipQueryRepositoryImpl()
        try:
            active_ownerships, _ = ownership_repo.list_all(
                unit_id=unit_id,
                user_id=authorized_by_user_id,
                status="active",
                include_deleted=False,
            )
            if active_ownerships:
                # User is an active owner — authorization valid
                return
        except Exception:
            pass

        # Check 2: Does this user have an authorization-granting role?
        from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
            CondominiumRoleQueryRepositoryImpl,
        )
        # First we need condominium_id from unit
        from library.dddpy.core_units.infrastructure.unit_query_repository import (
            UnitQueryRepositoryImpl,
        )
        try:
            unit_repo = UnitQueryRepositoryImpl()
            unit = unit_repo.get_by_id(unit_id)
            if not unit:
                return  # Unit validation already handled elsewhere

            role_repo = CondominiumRoleQueryRepositoryImpl()
            roles, _ = role_repo.list_all(
                user_id=authorized_by_user_id,
                condominium_id=unit.condominium_id,
                status="active",
                include_deleted=False,
            )
            AUTH_ROLES = {"super_admin", "condominium_admin", "board_member", "finance_reviewer"}
            for role in roles:
                if role.role in AUTH_ROLES:
                    return  # User has authorization-granting role
        except Exception:
            pass

        # No valid authorization found — raise
        from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import UnauthorizedOccupancy
        raise UnauthorizedOccupancy()

    def create(self, schema: CreateUnitOccupancySchema) -> UnitOccupancyEntity:
        logger.info(
            f"Delegating unit occupancy creation unit_id={schema.unit_id}, "
            f"user_id={schema.user_id}, occupancy_type_id={schema.occupancy_type_id}"
        )
        # Validate against catalog — NOT enum
        ot = self._get_occupancy_type_from_catalog(schema.occupancy_type_id)
        self._validate_status(schema.status)
        self._validate_unit_exists(schema.unit_id)
        self._validate_user_exists(schema.user_id)

        # Validate primary occupancy rule
        if schema.is_primary and not ot["allows_primary"]:
            raise ValueError(f"Occupancy type id={schema.occupancy_type_id} does not allow primary occupancy")
        if schema.is_primary:
            self._check_primary_conflict(schema.unit_id)

        # Phase 1d: validate authorized_by_user_id has real relation (owner or auth role)
        self._validate_authorized_by(schema.authorized_by_user_id, schema.unit_id)

        data = CreateUnitOccupancyData(
            unit_id=schema.unit_id,
            user_id=schema.user_id,
            occupancy_type_id=schema.occupancy_type_id,
            status=schema.status,
            start_date=schema.start_date,
            end_date=schema.end_date,
            is_primary=schema.is_primary,
            authorized_by_user_id=schema.authorized_by_user_id,
            notes=schema.notes,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateUnitOccupancySchema) -> Optional[UnitOccupancyEntity]:
        logger.info(f"Delegating unit occupancy update for id={id}")

        if schema.occupancy_type_id is not None:
            ot = self._get_occupancy_type_from_catalog(schema.occupancy_type_id)
            if schema.is_primary and not ot["allows_primary"]:
                raise ValueError(f"Occupancy type id={schema.occupancy_type_id} does not allow primary occupancy")
        if schema.status is not None:
            self._validate_status(schema.status)
        if schema.is_primary:
            self._check_primary_conflict(schema.unit_id or self.repository.get_unit_id(id), exclude_id=id)

        # Phase 1d: validate authorized_by_user_id has real relation (owner or auth role)
        unit_id_for_auth = getattr(schema, 'unit_id', None) if getattr(schema, 'unit_id', None) is not None else self.repository.get_unit_id(id)
        if unit_id_for_auth is not None:
            self._validate_authorized_by(schema.authorized_by_user_id, unit_id_for_auth)

        data = UpdateUnitOccupancyData(
            occupancy_type_id=schema.occupancy_type_id,
            status=schema.status,
            start_date=schema.start_date,
            end_date=schema.end_date,
            is_primary=schema.is_primary,
            authorized_by_user_id=schema.authorized_by_user_id,
            notes=schema.notes,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating unit occupancy soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating unit occupancy restore for id={id}")
        return self.repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Delegating unit occupancy hard delete for id={id}")
        return self.repository.hard_delete(id)