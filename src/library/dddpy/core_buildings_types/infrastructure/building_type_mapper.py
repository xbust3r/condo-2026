"""
BuildingType Mapper — transforms between DB model and Domain entity.
"""
from library.dddpy.core_buildings_types.infrastructure.dbbuildingtype import DBBuildingType
from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity


class BuildingTypeMapper:
    """Mapper para convertir entre DBBuildingType y BuildingTypeEntity."""

    @staticmethod
    def to_domain(db_type: DBBuildingType) -> BuildingTypeEntity:
        return BuildingTypeEntity(
            id=db_type.id,
            uuid=db_type.uuid,
            code=db_type.code,
            name=db_type.name,
            description=db_type.description,
            condominium_id=db_type.condominium_id,
            is_system=bool(db_type.is_system),
            sort_order=db_type.sort_order,
            status=db_type.status,
            created_at=db_type.created_at,
            updated_at=db_type.updated_at,
            deleted_at=db_type.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: BuildingTypeEntity) -> DBBuildingType:
        return DBBuildingType(
            id=entity.id,
            uuid=entity.uuid,
            code=entity.code,
            name=entity.name,
            description=entity.description,
            condominium_id=entity.condominium_id,
            is_system=int(entity.is_system),
            sort_order=entity.sort_order,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
