from typing import Optional
from decimal import Decimal

from library.dddpy.core_units.usecase.unit_cmd_schema import (
    CreateUnitSchema,
    UpdateUnitSchema,
)
from library.dddpy.core_units.domain.unit_cmd_repository import UnitCmdRepository
from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_data import CreateUnitData, UpdateUnitData
from library.dddpy.core_units.domain.unit_exception import OccupancyStatusNotAllowed
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitCmdUseCase")


class UnitCmdUseCase:

    VALID_OCCUPANCY = {"vacant", "occupied", "reserved", "maintenance", "blocked"}

    def __init__(self, repository: UnitCmdRepository):
        self.repository = repository
        logger.info("UnitCmdUseCase initialized")

    def _validate_occupancy_status(self, status: str) -> None:
        if status not in self.VALID_OCCUPANCY:
            raise OccupancyStatusNotAllowed(status)

    def _validate_unit_type(
        self,
        unit_type_id: Optional[int],
        building_id: int,
    ) -> None:
        """
        Validate unit_type_id against business rules for a given building.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global OR belong to the same condominium as the building

        Silent pass if unit_type_id is None.
        Raises DomainException on failure.
        """
        if unit_type_id is None:
            return
        from library.dddpy.core_buildings.infrastructure.building_query_repository import (
            BuildingQueryRepositoryImpl,
        )
        building_repo = BuildingQueryRepositoryImpl()
        building = building_repo.get_by_id(building_id)
        if not building:
            from library.dddpy.core_units.domain.unit_exception import BuildingNotFoundForUnit
            raise BuildingNotFoundForUnit()

        from library.dddpy.core_unit_types.usecase.unit_type_usecase import (
            UnitTypeUseCase,
        )
        UnitTypeUseCase().validate_for_unit_assignment(
            type_id=unit_type_id,
            condominium_id=building.condominium_id,
        )

    def _validate_building(self, building_id: int) -> None:
        """Validate building exists and is active."""
        try:
            from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
            BuildingUseCase().get_by_id(building_id)
        except Exception:
            from library.dddpy.core_units.domain.unit_exception import BuildingNotFoundForUnit
            raise BuildingNotFoundForUnit()

    def create(self, schema: CreateUnitSchema) -> UnitEntity:
        logger.info(
            f"Delegating unit creation unit_number={schema.unit_number}, "
            f"building_id={schema.building_id}"
        )
        self._validate_occupancy_status(schema.occupancy_status)
        self._validate_building(schema.building_id)
        self._validate_unit_type(schema.unit_type_id, schema.building_id)

        data = CreateUnitData(
            building_id=schema.building_id,
            unit_number=schema.unit_number,
            unit_type_id=schema.unit_type_id,
            code=schema.code,
            name=schema.name,
            description=schema.description,
            private_area=Decimal(str(schema.private_area)) if schema.private_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floor_number=schema.floor_number,
            floor_label=schema.floor_label,
            occupancy_status=schema.occupancy_status,
            sort_order=schema.sort_order,
            condominium_coefficient=Decimal(str(schema.condominium_coefficient)) if schema.condominium_coefficient is not None else None,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateUnitSchema) -> Optional[UnitEntity]:
        logger.info(f"Delegating unit update for id={id}")

        if schema.occupancy_status is not None:
            self._validate_occupancy_status(schema.occupancy_status)
        if schema.unit_type_id is not None:
            from library.dddpy.core_units.infrastructure.unit_query_repository import (
                UnitQueryRepositoryImpl,
            )
            unit_repo = UnitQueryRepositoryImpl()
            existing = unit_repo.get_by_id(id)
            if existing:
                self._validate_unit_type(schema.unit_type_id, existing.building_id)

        data = UpdateUnitData(
            unit_number=schema.unit_number,
            code=schema.code,
            name=schema.name,
            description=schema.description,
            unit_type_id=schema.unit_type_id,
            private_area=Decimal(str(schema.private_area)) if schema.private_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floor_number=schema.floor_number,
            floor_label=schema.floor_label,
            occupancy_status=schema.occupancy_status,
            sort_order=schema.sort_order,
            status=schema.status,
            condominium_coefficient=Decimal(str(schema.condominium_coefficient)) if schema.condominium_coefficient is not None else None,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating unit soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating unit restore for id={id}")
        return self.repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Delegating unit hard delete for id={id}")
        return self.repository.hard_delete(id)