from typing import Optional
from decimal import Decimal
from typing import Optional

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
    OwnershipPercentageSumExceeded,
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

    def _validate_percentage_sum(
        self,
        unit_id: int,
        new_percentage: float,
        exclude_id: Optional[int] = None,
    ) -> None:
        """
        Validates that adding new_percentage to active ownerships for unit_id
        does not exceed 100%.
        Raises OwnershipPercentageSumExceeded if the sum would exceed 100.
        """
        active = self.repository.find_active_by_unit(unit_id)
        current_sum = sum(float(o.ownership_percentage) for o in active)
        if exclude_id is not None:
            # Subtract the current value of the record being updated
            for o in active:
                if o.id == exclude_id:
                    current_sum -= float(o.ownership_percentage)
                    break
        proposed_sum = current_sum + new_percentage
        if proposed_sum > 100:
            raise OwnershipPercentageSumExceeded(
                unit_id, round(current_sum, 2), round(new_percentage, 2)
            )

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

        # Phase 1d: validate percentage sum does not exceed 100%
        self._validate_percentage_sum(schema.unit_id, schema.ownership_percentage)

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

        # Phase 1d: validate percentage sum on update if percentage is changing
        if schema.ownership_percentage is not None:
            # Get current entity to know unit_id
            existing = self.repository.get_by_id_any_status(id)
            if existing:
                self._validate_percentage_sum(
                    existing.unit_id,
                    schema.ownership_percentage,
                    exclude_id=id,
                )

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
