from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
from chalicelib.dddpy.core_buildings.domain.buildings_repository import BuildingsCmdRepository
from chalicelib.dddpy.core_buildings.usecase.buildings_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_cmd_usecase")


class BuildingsCmdUseCase:
    def __init__(self, repository: BuildingsCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateBuildingSchema) -> Buildings:
        logging.add_inside_method("create")
        logging.info(f"Creating building: {data.name}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateBuildingSchema) -> Buildings:
        logging.add_inside_method("update")
        logging.info(f"Updating building id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting building id: {id}")
        return self.repository.delete(id)
