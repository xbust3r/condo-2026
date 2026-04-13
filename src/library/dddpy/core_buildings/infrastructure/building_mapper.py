"""
Building Mapper - Transforma entre DB model y Domain entity.
"""
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_buildings.domain.building_entity import BuildingEntity


class BuildingMapper:
    """Mapper para convertir entre DBBuildings y BuildingEntity."""

    @staticmethod
    def to_domain(db_building: DBBuildings) -> BuildingEntity:
        """Convierte modelo DB a entidad de dominio."""
        return BuildingEntity(
            id=db_building.id,
            uuid=db_building.uuid,
            condominium_id=db_building.condominium_id,
            code=db_building.code,
            name=db_building.name,
            short_name=db_building.short_name,
            description=db_building.description,
            building_type_id=db_building.building_type_id,
            built_area=db_building.built_area,
            common_area=db_building.common_area,
            coefficient=db_building.coefficient,
            floors_count=db_building.floors_count,
            basements_count=db_building.basements_count,
            units_planned=db_building.units_planned,
            sort_order=db_building.sort_order,
            status=db_building.status,
            created_at=db_building.created_at,
            updated_at=db_building.updated_at,
            deleted_at=db_building.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: BuildingEntity) -> DBBuildings:
        """Convierte entidad de dominio a modelo DB."""
        return DBBuildings(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            code=entity.code,
            name=entity.name,
            short_name=entity.short_name,
            description=entity.description,
            building_type_id=entity.building_type_id,
            built_area=entity.built_area,
            common_area=entity.common_area,
            coefficient=entity.coefficient,
            floors_count=entity.floors_count,
            basements_count=entity.basements_count,
            units_planned=entity.units_planned,
            sort_order=entity.sort_order,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )