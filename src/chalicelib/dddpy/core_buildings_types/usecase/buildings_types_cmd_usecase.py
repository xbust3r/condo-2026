from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesCmdRepository
from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_cmd_schema import CreateBuildingTypeSchema, UpdateBuildingTypeSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_types_cmd_usecase")


class BuildingsTypesCmdUseCase:
    def __init__(self, repository: BuildingsTypesCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateBuildingTypeSchema) -> BuildingsTypes:
        logging.add_ins")
        logging.info(f"Creating buildingide_method("create type: {data.name}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateBuildingTypeSchema) -> BuildingsTypes:
        logging.add_inside_method("update")
        logging.info(f"Updating building type id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting building type id: {id}")
        return self.repository.delete(id)
