from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_repository import UnitysTypesCmdRepository
from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_cmd_schema import CreateUnityTypeSchema, UpdateUnityTypeSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unittys_types_cmd_usecase")


class UnitysTypesCmdUseCase:
    def __init__(self, repository: UnitysTypesCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateUnityTypeSchema) -> UnitysTypes:
        logging.add_inside_method("create")
        logging.info(f"Creating unity type: {data.name}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateUnityTypeSchema) -> UnitysTypes:
        logging.add_inside_method("update")
        logging.info(f"Updating unity type id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting unity type id: {id}")
        return self.repository.delete(id)
