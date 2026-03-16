# Mapper for Buildings
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.infrastructure.buildings import DBBuildings


class BuildingsMapper:
    
    @staticmethod
    def to_domain(db_building: DBBuildings) -> Buildings:
        return Buildings(
            id=db_building.id,
            name=db_building.name,
            code=db_building.code,
            description=db_building.description,
            size=float(db_building.size) if db_building.size else None,
            percentage=float(db_building.percentage) if db_building.percentage else None,
            type=db_building.type,
            condominium_id=db_building.condominium_id,
            building_type_id=db_building.building_type_id,
            status=db_building.status,
            created_at=db_building.created_at,
            updated_at=db_building.updated_at,
        )
