from typing import Optional, List
from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_types_query_usecase")


class BuildingsTypesQueryUseCase:
    def __init__(self, repository: BuildingsTypesQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting building type by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting building type by code: {code}")
        return self.repository.get_by_code(code)
    
    def get_all(self) -> List[BuildingsTypes]:
        logging.add_inside_method("get_all")
        logging.info("Getting all building types")
        return self.repository.get_all()
