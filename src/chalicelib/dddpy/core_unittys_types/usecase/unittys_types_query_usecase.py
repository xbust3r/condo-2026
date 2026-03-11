from typing import Optional, List
from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_repository import UnitysTypesQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unittys_types_query_usecase")


class UnitysTypesQueryUseCase:
    def __init__(self, repository: UnitysTypesQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[UnitysTypes]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting unity type by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_code(self, code: str) -> Optional[UnitysTypes]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting unity type by code: {code}")
        return self.repository.get_by_code(code)
    
    def get_all(self) -> List[UnitysTypes]:
        logging.add_inside_method("get_all")
        logging.info("Getting all unity types")
        return self.repository.get_all()
