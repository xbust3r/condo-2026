from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
from chalicelib.dddpy.users_residents.domain.residents_repository import UsersResidentsCmdRepository
from chalicelib.dddpy.users_residents.usecase.residents_cmd_schema import CreateResidentSchema, UpdateResidentSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("residents_cmd_usecase")


class UsersResidentsCmdUseCase:
    def __init__(self, repository: UsersResidentsCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateResidentSchema) -> UsersResidents:
        logging.add_inside_method("create")
        logging.info(f"Creating resident for user_id: {data.user_id}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateResidentSchema) -> UsersResidents:
        logging.add_inside_method("update")
        logging.info(f"Updating resident id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting resident id: {id}")
        return self.repository.delete(id)
