from typing import List, Optional
from library.dddpy.users.domain.users import Users, UsersRepository
from library.dddpy.users.usecase.cmd import CreateUsersCmdSchema, UpdateUsersCmdSchema

class UsersCmdUseCase:
    def __init__(self, repository: UsersRepository):
        self.repository = repository
    def create(self, schema: CreateUsersCmdSchema) -> Users:
        data = schema.model_dump()
        if data.get("password"):
            u = Users(id=0, first_name=data.get("first_name"), last_name=data.get("last_name"), email=data.get("email"))
            u.set_password(data.pop("password"))
            data["password"] = u.password
        return self.repository.create(data)
    def update(self, id: int, schema: UpdateUsersCmdSchema) -> Users:
        data = schema.model_dump(exclude_unset=True)
        if data.get("password"):
            u = Users(id=id, first_name="", last_name="", email="")
            u.set_password(data.pop("password"))
            data["password"] = u.password
        return self.repository.update(id, data)
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

class UsersQueryUseCase:
    def __init__(self, repository: UsersRepository):
        self.repository = repository
    def get_all(self) -> List[Users]:
        return self.repository.all()
    def get_by_id(self, id: int) -> Optional[Users]:
        return self.repository.get_by_id(id)
    def get_by_email(self, email: str) -> Optional[Users]:
        return self.repository.get_by_email(email)

class UsersUseCase:
    def __init__(self, repository: UsersRepository):
        self.cmd_use_case = UsersCmdUseCase(repository)
        self.query_use_case = UsersQueryUseCase(repository)
    def create(self, schema: CreateUsersCmdSchema) -> Users:
        return self.cmd_use_case.create(schema)
    def update(self, id: int, schema: UpdateUsersCmdSchema) -> Users:
        return self.cmd_use_case.update(id, schema)
    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)
    def get_all(self) -> List[Users]:
        return self.query_use_case.get_all()
    def get_by_id(self, id: int) -> Optional[Users]:
        return self.query_use_case.get_by_id(id)
    def get_by_email(self, email: str) -> Optional[Users]:
        return self.query_use_case.get_by_email(email)

def create_users_usecase():
    from library.dddpy.users.infrastructure.users import UsersCmdRepositoryImpl
    return UsersUseCase(UsersCmdRepositoryImpl())
