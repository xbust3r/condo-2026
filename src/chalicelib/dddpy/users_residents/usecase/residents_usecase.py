from typing import Optional, List
from chalicelib.dddpy.users_residents.usecase.residents_factory import (
    residents_cmd_usecase_factory,
    residents_query_usecase_factory,
)
from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
from chalicelib.dddpy.users_residents.domain.residents_success import SuccessMessages
from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("residents_usecase")


class UsersResidentsUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = residents_cmd_usecase_factory()
        self.query = residents_query_usecase_factory()
        logging.info("UsersResidentsUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_resident = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.RESIDENT_CREATED,
            data=new_resident.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_resident = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.RESIDENT_UPDATED,
            data=updated_resident.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.RESIDENT_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> UsersResidents:
        logging.add_inside_method("get_by_id")
        resident = self.query.get_by_id(id)
        if not resident:
            raise ResidentNotFoundException()
        return resident
    
    def get_by_user_id(self, user_id: int) -> UsersResidents:
        logging.add_inside_method("get_by_user_id")
        resident = self.query.get_by_user_id(user_id)
        if not resident:
            raise ResidentNotFoundException()
        return resident
    
    def get_all(self) -> List[UsersResidents]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
    
    def get_by_unity_id(self, unity_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_unity_id")
        return self.query.get_by_unity_id(unity_id)
    
    def get_by_building_id(self, building_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_building_id")
        return self.query.get_by_building_id(building_id)
    
    def get_by_condominium_id(self, condominium_id: int) -> List[UsersResidents]:
        logging.add_inside_method("get_by_condominium_id")
        return self.query.get_by_condominium_id(condominium_id)
    
    def get_by_status(self, status: str) -> List[UsersResidents]:
        logging.add_inside_method("get_by_status")
        return self.query.get_by_status(status)
