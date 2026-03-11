from typing import Optional, List
from chalicelib.dddpy.users.usecase.users_factory import (
    users_cmd_usecase_factory,
    users_query_usecase_factory,
)
from chalicelib.dddpy.users.domain.users import Users
from chalicelib.dddpy.users.domain.users_success import SuccessMessages
from chalicelib.dddpy.users.domain.users_exception import UserNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("users_usecase")


class UsersUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = users_cmd_usecase_factory()
        self.query = users_query_usecase_factory()
        logging.info("UsersUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_user = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.USER_CREATED,
            data=new_user.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_user = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.USER_UPDATED,
            data=updated_user.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.USER_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> Users:
        logging.add_inside_method("get_by_id")
        user = self.query.get_by_id(id)
        if not user:
            raise UserNotFoundException()
        return user
    
    def get_by_email(self, email: str) -> Users:
        logging.add_inside_method("get_by_email")
        user = self.query.get_by_email(email)
        if not user:
            raise UserNotFoundException()
        return user
    
    def get_all(self) -> List[Users]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
    
    def get_by_status(self, status: str) -> List[Users]:
        logging.add_inside_method("get_by_status")
        return self.query.get_by_status(status)
