from fastapi import APIRouter, HTTPException, status
from library.dddpy.users.usecase.cmd import CreateUsersCmdSchema, UpdateUsersCmdSchema
from library.dddpy.users.usecase import create_users_usecase
from library.dddpy.users.domain import UsersNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=ResponseSchema)
def create_user(schema: CreateUsersCmdSchema):
    usecase = create_users_usecase()
    user = usecase.create(schema)
    return ResponseSchema(success=True, message="User created", data=user.to_dict())

@router.get("", response_model=ResponseSchema)
def get_all_users():
    usecase = create_users_usecase()
    users = usecase.get_all()
    return ResponseSchema(success=True, data=[u.to_dict() for u in users])

@router.get("/{user_id}", response_model=ResponseSchema)
def get_user(user_id: int):
    usecase = create_users_usecase()
    try:
        user = usecase.get_by_id(user_id)
        return ResponseSchema(success=True, data=user.to_dict())
    except UsersNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{user_id}", response_model=ResponseSchema)
def update_user(user_id: int, schema: UpdateUsersCmdSchema):
    usecase = create_users_usecase()
    try:
        user = usecase.update(user_id, schema)
        return ResponseSchema(success=True, message="User updated", data=user.to_dict())
    except UsersNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{user_id}", response_model=ResponseSchema)
def delete_user(user_id: int):
    usecase = create_users_usecase()
    try:
        usecase.delete(user_id)
        return ResponseSchema(success=True, message="User deleted")
    except UsersNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
