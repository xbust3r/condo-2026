# Mapper for Buildings Types
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes


class BuildingsTypesMapper:
    
    @staticmethod
    def to_domain(db_type: DBBuildingsTypes) -> BuildingsTypes:
        return BuildingsTypes(
            id=db_type.id,
            name=db_type.name,
            code=db_type.code,
            description=db_type.description,
            status=db_type.status,
            created_at=db_type.created_at,
            updated_at=db_type.updated_at,
        )
