from typing import Optional, List
from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
from chalicelib.dddpy.core_condominiums.domain.condominiums_repository import CondominiumsQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("condominiums_query_usecase")


class CondominiumsQueryUseCase:
    def __init__(self, repository: CondominiumsQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Condominiums]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting condominium by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_code(self, code: str) -> Optional[Condominiums]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting condominium by code: {code}")
        return self.repository.get_by_code(code)
    
    def get_all(self) -> List[Condominiums]:
        logging.add_inside_method("get_all")
        logging.info("Getting all condominiums")
        return self.repository.get_all()
