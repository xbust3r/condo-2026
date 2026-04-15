from decimal import Decimal

from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import (
    CreateUnitOwnershipSchema,
    UpdateUnitOwnershipSchema,
)
from library.dddpy.core_unit_ownerships.domain.unit_ownership_cmd_repository import UnitOwnershipCmdRepository
from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_data import CreateUnitOwnershipData, UpdateUnitOwnershipData
from library.dddpy.core_unit_ownerships.domain.unit_ownership_exception import (
    InvalidOwnershipType,
    InvalidOwnershipStatus,
    InvalidOwnershipPercentage,
    UnitNotFoundForOwnership,
    UserNotFoundForOwnership,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipCmdUseCase")


class UnitOwnershipCmdUseCase:

    VALID_OWNERSHIP_TYPES = {"owner", "co_owner"}
    VALID_STATUSES = {"active", "inactive", "historical"}

    def __init__(self, repository: UnitOwnershipCmdRepository):
        self.repository = repository
        logger.info("UnitOwnershipCmdUseCase initialized")

    def _validate_ownership_type(self, ownership_type: str) -> None:
        if ownership_type not in self.VALID_OWNERSHIP_TYPES:
            raise InvalidOwnershipType(ownership_type)

    def _validate_status(self, status: str) -> None:
        if status not in self.VALID_STATUSES:
            raise InvalidOwnershipStatus(status)

    def _validate_unit_exists(self, unit_id: int) -> None:
        """Validate unit exists and is active."""
        try:
            from library.dddpy.core_units.infrastructure.unit_query_repository import (
                UnitQueryRepositoryImpl,
            )
            unit_repo = UnitQueryRepositoryImpl()
            unit = unit_repo.get_by_id(unit_id)
            if not unit:
                raise UnitNotFoundForOwnership()
        except Exception:
            raise UnitNotFoundForOwnership()

    def _validate_user_exists(self, user_id: int) -> None:
        """Validate user exists and is active."""
        try:
            from library.dddpy.users.infrastructure.user_query_repository import (
                UserQueryRepositoryImpl,
            )
            user_repo = UserQueryRepositoryImpl()
            user = user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundForOwnership()
        except Exception:
            raise UserNotFoundForOwnership()

    def create(self, schema: CreateUnitOwnershipSchema) -> UnitOwnershipEntity:
        logger.info(
            f"Delegating unit ownership creation unit_id={schema.unit_id}, "
            f"user_id={schema.user_id}, ownership_type={schema.ownership_type}"
        )
        self._validate_ownership_type(schema.ownership_type)
        self._validate_unit_exists(schema.unit_id)
        self._validate_user_exists(schema.user_id)

        if schema.ownership_percentage < 0 or schema.ownership_percentage > 100:
            raise InvalidOwnershipPercentage(
                "ownership_percentage must be between 0 and 100"
            )

        if schema.end_date is not None and schema.end_date < schema.start_date:
            raise InvalidOwnershipPercentage("end_date must be on or after start_date")

        data = CreateUnitOwnershipData(
            unit_id=schema.unit_id,
            user_id=schema.user_id,
            ownership_type=schema.ownership_type,
            ownership_percentage=Decimal(str(schema.ownership_percentage)),
            start_date=schema.start_date,
            end_date=schema.end_date,
            notes=schema.notes,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateUnitOwnershipSchema) -> UnitOwnershipEntity:
        logger.info(f"Delegating unit ownership update for id={id}")

        if schema.ownership_type is not None:
            self._validate_ownership_type(schema.ownership_type)
        if schema.status is not None:
            self._validate_status(schema.status)
        if schema.ownership_percentage is not None:
            if schema.ownership_percentage < 0 or schema.ownership_percentage > 100:
                raise InvalidOwnershipPercentage(
                    "ownership_percentage must be between 0 and 100"
                )
        if schema.end_date is not None and schema.start_date is not None:
            if schema.end_date < schema.start_date:
                raise InvalidOwnershipPercentage("end_date must be on or after start_date")

        data = UpdateUnitOwnershipData(
            ownership_type=schema.ownership_type,
            ownership_percentage=(
                Decimal(str(schema.ownership_percentage))
                if schema.ownership_percentage is not None
                else None
            ),
            status=schema.status,
            start_date=schema.start_date,
            end_date=schema.end_date,
            notes=schema.notes,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating unit ownership soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating unit ownership restore for id={id}")
        return self.repository.restore(id)
