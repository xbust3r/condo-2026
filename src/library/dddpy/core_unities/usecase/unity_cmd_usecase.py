from typing import Optional
from decimal import Decimal

from library.dddpy.core_unities.usecase.unity_cmd_schema import (
    CreateUnitySchema,
    UpdateUnitySchema,
)
from library.dddpy.core_unities.domain.unity_cmd_repository import UnityCmdRepository
from library.dddpy.core_unities.domain.unity_entity import UnityEntity
from library.dddpy.core_unities.domain.unity_data import CreateUnityData, UpdateUnityData
from library.dddpy.core_unities.domain.unity_exception import OccupancyStatusNotAllowed
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityCmdUseCase")


class UnityCmdUseCase:

    VALID_OCCUPANCY = {"vacant", "occupied", "reserved", "maintenance", "blocked"}

    def __init__(self, repository: UnityCmdRepository):
        self.repository = repository
        logger.info("UnityCmdUseCase initialized")

    def _validate_occupancy_status(self, status: str) -> None:
        if status not in self.VALID_OCCUPANCY:
            raise OccupancyStatusNotAllowed(status)

    def _validate_unity_type(
        self,
        unity_type_id: Optional[int],
        building_id: int,
    ) -> None:
        """
        Validate unity_type_id against business rules for a given building.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global OR belong to the same condominium as the building

        Silent pass if unity_type_id is None.
        Raises DomainException on failure.
        """
        if unity_type_id is None:
            return
        # Resolve building's condominium_id for scope validation
        from library.dddpy.core_buildings.infrastructure.building_query_repository import (
            BuildingQueryRepositoryImpl,
        )
        building_repo = BuildingQueryRepositoryImpl()
        building = building_repo.get_by_id(building_id)
        if not building:
            from library.dddpy.core_unities.domain.unity_exception import BuildingNotFoundForUnity
            raise BuildingNotFoundForUnity()

        from library.dddpy.core_unities_types.usecase.unity_type_usecase import (
            UnityTypeUseCase,
        )
        UnityTypeUseCase().validate_for_unity_assignment(
            type_id=unity_type_id,
            condominium_id=building.condominium_id,
        )

    def _validate_building(self, building_id: int) -> None:
        """Validate building exists and is active. Silent pass if not implemented yet."""
        try:
            from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
            BuildingUseCase().get_by_id(building_id)
        except Exception:
            from library.dddpy.core_unities.domain.unity_exception import BuildingNotFoundForUnity
            raise BuildingNotFoundForUnity()

    def create(self, schema: CreateUnitySchema) -> UnityEntity:
        logger.info(
            f"Delegating unity creation unit_number={schema.unit_number}, "
            f"building_id={schema.building_id}"
        )
        self._validate_occupancy_status(schema.occupancy_status)
        self._validate_building(schema.building_id)
        self._validate_unity_type(schema.unity_type_id, schema.building_id)

        data = CreateUnityData(
            building_id=schema.building_id,
            unit_number=schema.unit_number,
            unity_type_id=schema.unity_type_id,
            code=schema.code,
            name=schema.name,
            description=schema.description,
            private_area=Decimal(str(schema.private_area)) if schema.private_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floor_number=schema.floor_number,
            floor_label=schema.floor_label,
            occupancy_status=schema.occupancy_status,
            sort_order=schema.sort_order,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateUnitySchema) -> Optional[UnityEntity]:
        logger.info(f"Delegating unity update for id={id}")

        if schema.occupancy_status is not None:
            self._validate_occupancy_status(schema.occupancy_status)
        if schema.unity_type_id is not None:
            # Get existing unity to find its building → condominium_id
            from library.dddpy.core_unities.infrastructure.unity_query_repository import (
                UnityQueryRepositoryImpl,
            )
            unity_repo = UnityQueryRepositoryImpl()
            existing = unity_repo.get_by_id(id)
            if existing:
                self._validate_unity_type(schema.unity_type_id, existing.building_id)

        data = UpdateUnityData(
            unit_number=schema.unit_number,
            code=schema.code,
            name=schema.name,
            description=schema.description,
            unity_type_id=schema.unity_type_id,
            private_area=Decimal(str(schema.private_area)) if schema.private_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floor_number=schema.floor_number,
            floor_label=schema.floor_label,
            occupancy_status=schema.occupancy_status,
            sort_order=schema.sort_order,
            status=schema.status,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating unity soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating unity restore for id={id}")
        return self.repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Delegating unity hard delete for id={id}")
        return self.repository.hard_delete(id)
