from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
from chalicelib.dddpy.core_unitys.domain.unitys_repository import UnitysCmdRepository
from chalicelib.dddpy.core_unitys.usecase.unitys_cmd_schema import CreateUnitySchema, UpdateUnitySchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unitys_cmd_usecase")


class UnitysCmdUseCase:
    def __init__(self, repository: UnitysCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateUnitySchema) -> Unitys:
        logging.add_inside_method("create")
        logging.info(f"Creating unity: {data.name}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateUnitySchema) -> Unitys:
        logging.add_inside_method("update")
        logging.info(f"Updating unity id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting unity id: {id}")
        return self.repository.delete(id)
