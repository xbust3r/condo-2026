from typing import Optional, List
from chalicelib.dddpy.core_unitys.usecase.unitys_factory import (
    unitys_cmd_usecase_factory,
    unitys_query_usecase_factory,
)
from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
from chalicelib.dddpy.core_unitys.domain.unitys_success import SuccessMessages
from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnityNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unitys_usecase")


class UnitysUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = unitys_cmd_usecase_factory()
        self.query = unitys_query_usecase_factory()
        logging.info("UnitysUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_unity = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.UNITY_CREATED,
            data=new_unity.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_unity = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.UNITY_UPDATED,
            data=updated_unity.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.UNITY_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> Unitys:
        logging.add_inside_method("get_by_id")
        unity = self.query.get_by_id(id)
        if not unity:
            raise UnityNotFoundException()
        return unity
    
    def get_by_code(self, code: str) -> Unitys:
        logging.add_inside_method("get_by_code")
        unity = self.query.get_by_code(code)
        if not unity:
            raise UnityNotFoundException()
        return unity
    
    def get_all(self) -> List[Unitys]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
    
    def get_by_building_id(self, building_id: int) -> List[Unitys]:
        logging.add_inside_method("get_by_building_id")
        return self.query.get_by_building_id(building_id)
