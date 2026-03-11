from typing import Optional, List
from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_factory import (
    unittys_types_cmd_usecase_factory,
    unittys_types_query_usecase_factory,
)
from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_success import SuccessMessages
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import UnityTypeNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unittys_types_usecase")


class UnitysTypesUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = unittys_types_cmd_usecase_factory()
        self.query = unittys_types_query_usecase_factory()
        logging.info("UnitysTypesUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_unity_type = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.UNITY_TYPE_CREATED,
            data=new_unity_type.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_unity_type = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.UNITY_TYPE_UPDATED,
            data=updated_unity_type.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.UNITY_TYPE_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> UnitysTypes:
        logging.add_inside_method("get_by_id")
        unity_type = self.query.get_by_id(id)
        if not unity_type:
            raise UnityTypeNotFoundException()
        return unity_type
    
    def get_by_code(self, code: str) -> UnitysTypes:
        logging.add_inside_method("get_by_code")
        unity_type = self.query.get_by_code(code)
        if not unity_type:
            raise UnityTypeNotFoundException()
        return unity_type
    
    def get_all(self) -> List[UnitysTypes]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
