from typing import Optional
from typing import Optional, List

from library.dddpy.core_condominiums.domain.condominium_query_repository import CondominiumQueryRepository
from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumQueryUseCase")


class CondominiumQueryUseCase:

    def __init__(self, repository: CondominiumQueryRepository):
        self.repository = repository
        logger.info("CondominiumQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium fetch by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium fetch by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_by_code(self, code: str) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium fetch by code={code}")
        return self.repository.get_by_code(code)

    def get_by_name(self, name: str) -> Optional[CondominiumEntity]:
        logger.info(f"Delegating condominium fetch by name={name}")
        return self.repository.get_by_name(name)

    def list_all(self, skip: int = 0, limit: int = 100, status: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, include_deleted: bool = False) -> tuple[List[CondominiumEntity], int]:
        logger.info(f"Delegating condominium list_all (skip={skip}, limit={limit}, status={status}, city={city}, country={country}, include_deleted={include_deleted})")
        return self.repository.list_all(skip=skip, limit=limit, status=status, city=city, country=country, include_deleted=include_deleted)


    def get_by_id_any_status(self, id: int) -> Optional[CondominiumEntity]:
        """"Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Delegating condominium fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)
