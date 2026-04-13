from typing import Optional
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

    def create(self, schema: CreateBuildingSchema) -> BuildingEntity:
        logger.info(f"Delegating building creation for code={schema.code}, condominium_id={schema.condominium_id}")
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