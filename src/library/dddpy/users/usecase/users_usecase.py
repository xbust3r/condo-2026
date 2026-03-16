# Users Schemas and Use Cases
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from library.dddpy.users.domain.users import Users, UsersRepository
from library.dddpy.users.infrastructure.users import UsersCmdRepositoryImpl


class CreateUsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: int = Field(default=1, ge=0, le=2)


class UpdateUsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[int] = Field(None, ge=0, le=2)


class UsersUseCase:
    """Facade for Users"""
    
    def __init__(self, repository: UsersRepository = None):
        self.repository = repository or UsersCmdRepositoryImpl()

    def create(self, schema: CreateUsersSchema) -> Users:
        data = schema.model_dump()
        # Hash password if provided
        if data.get("password"):
            user = Users(id=0, first_name=data.get("first_name"), last_name=data.get("last_name"), email=data.get("email"))
            user.set_password(data.pop("password"))
            data["password"] = user.password
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateUsersSchema) -> Users:
        data = schema.model_dump(exclude_unset=True)
        # Hash password if provided
        if data.get("password"):
            user = Users(id=id, first_name="", last_name="", email="")
            user.set_password(data.pop("password"))
            data["password"] = user.password
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def get_all(self) -> List[Users]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Users:
        return self.repository.get_by_id(id)

    def get_by_email(self, email: str) -> Users:
        return self.repository.get_by_email(email)


def create_users_usecase() -> UsersUseCase:
    return UsersUseCase()
