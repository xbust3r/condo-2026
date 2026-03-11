from typing import Optional, List
from chalicelib.dddpy.core_condominiums.usecase.condominiums_factory import (
    condominiums_cmd_usecase_factory,
    condominiums_query_usecase_factory,
)
from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
from chalicelib.dddpy.core_condominiums.domain.condominiums_success import SuccessMessages
from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import CondominiumNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("condominiums_usecase")


class CondominiumsUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = condominiums_cmd_usecase_factory()
        self.query = condominiums_query_usecase_factory()
        logging.info("CondominiumsUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_condominium = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.CONDOMINIUM_CREATED,
            data=new_condominium.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_condominium = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.CONDOMINIUM_UPDATED,
            data=updated_condominium.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.CONDOMINIUM_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> Condominiums:
        logging.add_inside_method("get_by_id")
        condominium = self.query.get_by_id(id)
        if not condominium:
            raise CondominiumNotFoundException()
        return condominium
    
    def get_by_code(self, code: str) -> Condominiums:
        logging.add_inside_method("get_by_code")
        condominium = self.query.get_by_code(code)
        if not condominium:
            raise CondominiumNotFoundException()
        return condominium
    
    def get_all(self) -> List[Condominiums]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
