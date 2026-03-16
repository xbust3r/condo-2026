# Buildings Query Use Case
from typing import List, Optional
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsQueryUseCase")


class BuildingsQueryUseCase:
    def __init__(self, repository: BuildingsRepository):
        self.repository = repository

    def get_all(self) -> List[Buildings]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Optional[Buildings]:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Buildings]:
        return self.repository.get_by_code(code)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        return self.repository.get_by_condominium(condominium_id)
