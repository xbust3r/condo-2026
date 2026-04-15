from typing import Optional

from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import (
    CreateUnitOccupancySchema,
    UpdateUnitOccupancySchema,
)
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_cmd_repository import UnitOccupancyCmdRepository
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_data import CreateUnitOccupancyData, UpdateUnitOccupancyData
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import (
    InvalidOccupancyType,
    InvalidOccupancyStatus,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyCmdUseCase")


class UnitOccupancyCmdUseCase:

    VALID_OCCUPANCY_TYPES = {"resident_owner", "tenant", "family_member", "office_user", "occasional_user"}
    VALID_STATUSES = {"active", "inactive", "historical", "pending"}

    def __init__(self, repository: UnitOccupancyCmdRepository):
        self.repository = repository
        logger.info("UnitOccupancyCmdUseCase initialized")

    def _validate_occupancy_type(self, occupancy_type: str) -> None:
        if occupancy_type not in self.VALID_OCCUPANCY_TYPES:
            raise InvalidOccupancyType(occupancy_type)

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

    def create(self, schema: CreateUnitOccupancySchema) -> UnitOccupancyEntity:
        logger.info(
            f"Delegating unit occupancy creation unit_id={schema.unit_id}, "
            f"user_id={schema.user_id}, occupancy_type={schema.occupancy_type}"
        )
        self._validate_occupancy_type(schema.occupancy_type)
        self._validate_status(schema.status)
        self._validate_unit_exists(schema.unit_id)
        self._validate_user_exists(schema.user_id)

        data = CreateUnitOccupancyData(
            unit_id=schema.unit_id,
            user_id=schema.user_id,
            occupancy_type=schema.occupancy_type,
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

        if schema.occupancy_type is not None:
            self._validate_occupancy_type(schema.occupancy_type)
        if schema.status is not None:
            self._validate_status(schema.status)

        data = UpdateUnitOccupancyData(
            occupancy_type=schema.occupancy_type,
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
