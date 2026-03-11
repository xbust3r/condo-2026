from chalicelib.dddpy.users.domain.users import Users
from chalicelib.dddpy.users.domain.users_repository import UsersCmdRepository
from chalicelib.dddpy.users.usecase.users_cmd_schema import CreateUserSchema, UpdateUserSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("users_cmd_usecase")


class UsersCmdUseCase:
    def __init__(self, repository: UsersCmdRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def create(self, data: CreateUserSchema) -> Users:
        logging.add_inside_method("create")
        logging.info(f"Creating user: {data.email}")
        return self.repository.create(data.model_dump())
    
    def update(self, id: int, data: UpdateUserSchema) -> Users:
        logging.add_inside_method("update")
        logging.info(f"Updating user id: {id}")
        return self.repository.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int) -> bool:
        logging.add_inside_method("delete")
        logging.info(f"Deleting user id: {id}")
        return self.repository.delete(id)
