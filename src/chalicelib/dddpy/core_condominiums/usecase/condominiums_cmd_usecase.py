from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
from chalicelib.dddpy.core_condominiums.domain.condominiums_repository import CondominiumsCmdRepository
from chalicelib.dddpy.core_condominiums.usecase.condominiums_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("condominiums_cmd_usecase")


class CondominiumsCmdUseCase:
    def __init__(self, repository: CondominiumsCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateCondominiumSchema) -> Condominiums:
        logging.add_inside_method("create")
        logging.info(f"Creating condominium: {data.name}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateCondominiumSchema) -> Condominiums:
        logging.add_inside_method("update")
        logging.info(f"Updating condominium id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting condominium id: {id}")
        return self.repository.delete(id)
