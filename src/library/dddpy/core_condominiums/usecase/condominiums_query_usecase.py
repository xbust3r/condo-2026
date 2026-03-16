# Condominium Query Use Case
from typing import List, Optional
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.shared.logging.logging import Logger

logger = Logger("CondominiumQueryUseCase")


class CondominiumQueryUseCase:
    
    def __init__(self, repository: CondominiumRepository):
        self.repository = repository

    def get_all(self) -> List[Condominium]:
        logger.info("Getting all condominiums")
        return self.repository.all()

    def get_by_id(self, id: int) -> Optional[Condominium]:
        logger.info(f"Getting condominium by id: {id}")
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Condominium]:
        logger.info(f"Getting condominium by code: {code}")
        return self.repository.get_by_code(code)

    def get_by_status(self, status: int) -> List[Condominium]:
        logger.info(f"Getting condominiums by status: {status}")
        return self.repository.get_by_status(status)
