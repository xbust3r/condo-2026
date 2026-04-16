from typing import Optional, Dict, Any
from decimal import Decimal

from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from library.dddpy.core_buildings.domain.building_cmd_repository import BuildingCmdRepository
from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_data import CreateBuildingData, UpdateBuildingData
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingCmdUseCase")


class BuildingCmdUseCase:

    def __init__(self, repository: BuildingCmdRepository):
        self.repository = repository
        logger.info("BuildingCmdUseCase initialized")

    def _validate_building_type(
        self,
        building_type_id: Optional[int],
        condominium_id: int,
    ) -> None:
        """
        Validate building_type_id against business rules.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global OR belong to the same condominium

        Raises DomainException on failure. Silent pass if building_type_id is None.
        """
        if building_type_id is None:
            return

        # Import here to avoid circular dependency
        from library.dddpy.core_buildings_types.usecase.building_type_usecase import (
            BuildingTypeUseCase,
        )
        BuildingTypeUseCase().validate_for_building_assignment(
            type_id=building_type_id,
            condominium_id=condominium_id,
        )

    def create(self, schema: CreateBuildingSchema) -> BuildingEntity:
        logger.info(
            f"Delegating building creation for code={schema.code}, "
            f"condominium_id={schema.condominium_id}"
        )
        # Validate building_type_id before any DB write
        self._validate_building_type(schema.building_type_id, schema.condominium_id)

        data = CreateBuildingData(
            condominium_id=schema.condominium_id,
            code=schema.code,
            name=schema.name,
            short_name=schema.short_name,
            description=schema.description,
            building_type_id=schema.building_type_id,
            built_area=Decimal(str(schema.built_area)) if schema.built_area is not None else None,
            common_area=Decimal(str(schema.common_area)) if schema.common_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floors_count=schema.floors_count,
            basements_count=schema.basements_count,
            units_planned=schema.units_planned,
            sort_order=schema.sort_order,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateBuildingSchema) -> Optional[BuildingEntity]:
        logger.info(f"Delegating building update for id={id}")

        # When updating building_type_id, validate the new value.
        # Get the current condominium_id so we can validate scope.
        if schema.building_type_id is not None:
            from library.dddpy.core_buildings.infrastructure.building_query_repository import (
                BuildingQueryRepositoryImpl,
            )
            query_repo = BuildingQueryRepositoryImpl()
            existing = query_repo.get_by_id(id)
            if existing:
                self._validate_building_type(schema.building_type_id, existing.condominium_id)

        data = UpdateBuildingData(
            name=schema.name,
            short_name=schema.short_name,
            description=schema.description,
            building_type_id=schema.building_type_id,
            built_area=Decimal(str(schema.built_area)) if schema.built_area is not None else None,
            common_area=Decimal(str(schema.common_area)) if schema.common_area is not None else None,
            coefficient=Decimal(str(schema.coefficient)) if schema.coefficient is not None else None,
            floors_count=schema.floors_count,
            basements_count=schema.basements_count,
            units_planned=schema.units_planned,
            sort_order=schema.sort_order,
            status=schema.status,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating building soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating building restore for id={id}")
        return self.repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Delegating building hard delete for id={id}")
        return self.repository.hard_delete(id)

    def update_computed_fields(self, id: int, stats: Dict[str, Any]) -> Optional[BuildingEntity]:
        logger.info(f"Delegating computed fields update for building id={id}")
        return self.repository.update_computed_fields(id, stats)
