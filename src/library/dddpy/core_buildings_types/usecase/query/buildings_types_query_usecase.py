from typing import List, Optional
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository

class BuildingsTypesQueryUseCase:
    def __init__(self, repository: BuildingsTypesRepository):
        self.repository = repository

    def get_all(self) -> List[BuildingsTypes]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        return self.repository.get_by_code(code)
